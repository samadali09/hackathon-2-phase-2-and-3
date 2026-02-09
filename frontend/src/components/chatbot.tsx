import React, { useState } from 'react';

interface ChatBotProps {
  userId: string;
  onTasksChanged?: () => void;
}

export const ChatBot: React.FC<ChatBotProps> = ({ userId, onTasksChanged }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: string, text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    const userMsg = { role: 'user', text: message };
    setChatHistory([...chatHistory, userMsg]);
    setMessage('');

    try {
      const response = await fetch(`http://localhost:8000/api/${userId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text }),
      });
      const data = await response.json();
      setChatHistory(prev => [...prev, { role: 'ai', text: data.response }]);

      // If tasks may have changed (e.g., "add task", "list tasks"), refresh them in the dashboard
      if (onTasksChanged) {
        onTasksChanged();
      }
    } catch (error) {
      console.error("Chat Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {/* Floating Button */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="bg-purple-600 p-4 rounded-full shadow-lg hover:bg-purple-700 transition"
      >
        💬
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="absolute bottom-16 right-0 w-80 h-96 bg-gray-900 border border-gray-700 rounded-lg flex flex-col shadow-2xl">
          <div className="p-3 border-b border-gray-700 font-bold bg-gray-800 rounded-t-lg">TaskFlow AI</div>
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {chatHistory.map((msg, i) => (
              <div key={i} className={`p-2 rounded-lg max-w-[80%] ${msg.role === 'user' ? 'bg-purple-600 ml-auto' : 'bg-gray-700'}`}>
                {msg.text}
              </div>
            ))}
            {loading && <div className="text-gray-500 animate-pulse text-sm">Thinking...</div>}
          </div>
          <div className="p-2 border-t border-gray-700 flex gap-2">
            <input 
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 bg-gray-800 p-2 rounded outline-none border border-gray-600 focus:border-purple-500"
              placeholder="Ask me to add a task..."
            />
            <button onClick={sendMessage} className="bg-purple-600 px-3 rounded">Send</button>
          </div>
        </div>
      )}
    </div>
  );
};