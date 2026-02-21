import { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sessionId = "user-session-1";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    const res = await axios.post(`${API}/chat`, {
      session_id: sessionId,
      question: input,
    });

    const taskId = res.data.task_id;

    pollResult(taskId);
  };

  const pollResult = (taskId) => {
    const interval = setInterval(async () => {
      const res = await axios.get(`${API}/result/${taskId}`);

      if (res.data.status === "completed") {
        const botMessage = {
          role: "bot",
          text: res.data.result,
        };

        setMessages((prev) => [...prev, botMessage]);
        setLoading(false);
        clearInterval(interval);
      }

      if (res.data.status === "failed") {
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 flex flex-col">
      
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-lg p-4 rounded-2xl ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-gray-800 border border-gray-700"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-800 p-4 rounded-2xl border border-gray-700 w-fit">
            Thinking...
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-800 bg-gray-900 flex gap-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
        />

        <button
          onClick={sendMessage}
          className="bg-green-600 hover:bg-green-500 px-6 py-2 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}