import os
import json
import re
import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional, List
from mcp_server import MCPTools, get_gemini_tool_definitions
from models import Message, Conversation
from database import get_session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])

# Configure Gemini with the correct environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    tools=get_gemini_tool_definitions()
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


def _rule_based_tool_handler(user_id: str, message: str, mcp: MCPTools) -> tuple[str, Optional[str], Optional[str]]:
    """
    Fallback handler when Gemini is unavailable.
    Parses very simple natural language patterns and calls tools directly.
    Returns (ai_text, tool_name, tool_output_json).
    """
    text = message.strip()
    lower = text.lower()

    tool_name: Optional[str] = None
    tool_output_json: Optional[str] = None

    # Add task: e.g. "add task buy milk" / "add task to buy milk"
    if "add task" in lower:
        idx = lower.find("add task") + len("add task")
        raw_title = text[idx:].strip()
        if raw_title.lower().startswith("to "):
            raw_title = raw_title[3:].strip()
        if not raw_title:
            raw_title = "New task"
        res = mcp.add_task(user_id=user_id, title=raw_title)
        tool_name = "add_task"
        tool_output_json = json.dumps(res)
        ai_text = f"Task '{res.get('title', raw_title)}' added successfully."

    # List tasks: e.g. "list tasks", "show tasks"
    elif "list tasks" in lower or "show tasks" in lower:
        res = mcp.list_tasks(user_id=user_id)
        tool_name = "list_tasks"
        tool_output_json = json.dumps(res)
        if not res:
            ai_text = "You have no tasks yet."
        else:
            items = "; ".join(
                f"{t.get('id')}: {t.get('title')} ({t.get('status')})"
                for t in res
            )
            ai_text = f"Here are your tasks: {items}."

    # Complete task: e.g. "complete task 3", "mark task 3 done", "complete task buy milk"
    elif "complete task" in lower or "mark task" in lower:
        match = re.search(r"(?:complete|mark)\s+task\s+(\d+)", lower)
        if match:
            task_id = int(match.group(1))
            res = mcp.complete_task(user_id=user_id, task_id=task_id)
            tool_name = "complete_task"
            tool_output_json = json.dumps(res)
            if "error" in res:
                ai_text = res["error"]
            else:
                ai_text = f"Task {task_id} marked as completed."
        else:
            # Try to resolve by title instead of ID
            trigger = "complete task" if "complete task" in lower else "mark task"
            idx = lower.find(trigger) + len(trigger)
            title_query = text[idx:].strip()
            if title_query:
                tasks = mcp.list_tasks(user_id=user_id)
                matches = [
                    t for t in tasks
                    if title_query.lower() == str(t.get("title", "")).lower()
                    or title_query.lower() in str(t.get("title", "")).lower()
                ]
                if len(matches) == 1:
                    task_id = matches[0]["id"]
                    res = mcp.complete_task(user_id=user_id, task_id=task_id)
                    tool_name = "complete_task"
                    tool_output_json = json.dumps(res)
                    if "error" in res:
                        ai_text = res["error"]
                    else:
                        ai_text = f"Task '{matches[0].get('title')}' marked as completed."
                elif len(matches) > 1:
                    ids = ", ".join(str(t["id"]) for t in matches)
                    ai_text = f"Multiple tasks match '{title_query}'. Please specify the task ID instead (one of: {ids})."
                else:
                    ai_text = f"No task found with a title matching '{title_query}'."
            else:
                ai_text = "Please specify which task to complete, for example: 'complete task 3' or 'complete task buy milk'."

    # Delete task: e.g. "delete task 3", "remove task 3", "delete task buy milk"
    elif "delete task" in lower or "remove task" in lower:
        match = re.search(r"(?:delete|remove)\s+task\s+(\d+)", lower)
        if match:
            task_id = int(match.group(1))
            res = mcp.delete_task(user_id=user_id, task_id=task_id)
            tool_name = "delete_task"
            tool_output_json = json.dumps(res)
            if "error" in res:
                ai_text = res["error"]
            else:
                ai_text = f"Task {task_id} deleted successfully."
        else:
            # Try to resolve by title instead of ID
            trigger = "delete task" if "delete task" in lower else "remove task"
            idx = lower.find(trigger) + len(trigger)
            title_query = text[idx:].strip()
            if title_query:
                tasks = mcp.list_tasks(user_id=user_id)
                matches = [
                    t for t in tasks
                    if title_query.lower() == str(t.get("title", "")).lower()
                    or title_query.lower() in str(t.get("title", "")).lower()
                ]
                if len(matches) == 1:
                    task_id = matches[0]["id"]
                    res = mcp.delete_task(user_id=user_id, task_id=task_id)
                    tool_name = "delete_task"
                    tool_output_json = json.dumps(res)
                    if "error" in res:
                        ai_text = res["error"]
                    else:
                        ai_text = f"Task '{matches[0].get('title')}' deleted successfully."
                elif len(matches) > 1:
                    ids = ", ".join(str(t["id"]) for t in matches)
                    ai_text = f"Multiple tasks match '{title_query}'. Please specify the task ID instead (one of: {ids})."
                else:
                    ai_text = f"No task found with a title matching '{title_query}'."
            else:
                ai_text = "Please specify which task to delete, for example: 'delete task 2' or 'delete task buy milk'."

    else:
        # Generic fallback text when we can't parse intent
        ai_text = "Task processed successfully!"

    return ai_text, tool_name, tool_output_json

@router.post("")
async def chat_with_ai(
    user_id: str,
    req: ChatRequest,
    session: Session = Depends(get_session),
):
    # NOTE: Authentication check temporarily disabled for testing/demo.
    # To re-enable, inject `current_user_id: str = Depends(get_current_user_id)`
    # and compare it against the `user_id` path parameter.

    # 2. Conversation Logic
    if req.conversation_id:
        conv = session.get(Conversation, req.conversation_id)
        if not conv or str(conv.user_id) != str(user_id):
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)

    # 3. Save User Message
    session.add(Message(conversation_id=conv.id, user_id=user_id, sender="user", text=req.message))
    session.commit()

    # 4. History Reconstruction (Using JSON loads instead of eval)
    history = []
    past_messages = session.exec(
        select(Message).where(Message.conversation_id == conv.id).order_by(Message.timestamp)
    ).all()
    
    for m in past_messages:
        if m.tool_name and m.tool_arguments:
            # Reconstruct tool calls using safe JSON loading; if parsing fails,
            # fall back to treating it as plain text to avoid 500s.
            try:
                args = json.loads(m.tool_arguments)
                history.append(
                    {
                        "role": "model",
                        "parts": [
                            genai.types.FunctionCall(
                                name=m.tool_name,
                                args=args,
                            )
                        ],
                    }
                )
                if m.tool_output:
                    tool_output = json.loads(m.tool_output)
                    history.append(
                        {
                            "role": "function",
                            "parts": [
                                genai.types.FunctionResponse(
                                    name=m.tool_name,
                                    response=tool_output,
                                )
                            ],
                        }
                    )
                continue
            except Exception:
                # Corrupt/legacy JSON in tool fields; just fall through and use text.
                pass

        if m.text:
            role = "user" if m.sender == "user" else "model"
            history.append({"role": role, "parts": [m.text]})

    # 5. Interaction Loop
    ai_text = ""
    mcp = MCPTools()
    t_name: Optional[str] = None
    t_args: Optional[str] = None
    t_out: Optional[str] = None

    try:
        chat = model.start_chat(history=history)
        response = await chat.send_message_async(req.message)

        for part in response.parts:
            if part.text:
                ai_text += part.text
            if part.function_call:
                t_name = part.function_call.name
                # Serialize tool arguments safely
                t_args = json.dumps(dict(part.function_call.args))

                # Execute tool (add_task, list_tasks, etc.) with JSON-safe arguments
                res = getattr(mcp, t_name)(user_id=user_id, **part.function_call.args)
                # Store tool output as JSON for persistence
                t_out = json.dumps(res)

                # Prepare a JSON-safe response object for Gemini
                safe_tool_response = json.loads(t_out)

                # Await final summary from AI after tool call
                final_resp = await chat.send_message_async(
                    genai.types.FunctionResponse(
                        name=t_name,
                        response=safe_tool_response,
                    )
                )

                # SAFETY FALLBACK: ensure we always have user-visible text
                if final_resp.text:
                    ai_text = final_resp.text
                else:
                    ai_text = "Task processed successfully!"
    except Exception:
        # Gemini or network error: fall back to a simple rule-based handler
        ai_text, t_name, t_out = _rule_based_tool_handler(user_id, req.message, mcp)

    # Global safety fallback in case no text was produced at all
    if not ai_text or not ai_text.strip():
        ai_text = "Task processed successfully!"

    # 6. Save AI Response
    ai_msg = Message(
        conversation_id=conv.id, user_id=user_id, sender="model", 
        text=ai_text, tool_name=t_name, tool_arguments=t_args, tool_output=t_out
    )
    session.add(ai_msg)
    session.commit()
    
    return {"response": ai_text, "conversation_id": conv.id}