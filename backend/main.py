import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import create_db_and_tables
from routes import router as tasks_router
from auth import auth_router
from chat_routes import router as chat_router

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="TaskFlow API")

# Strict CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://todoapp-ten-sable.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(chat_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
