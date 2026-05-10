// frontend/src/App.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Send, FileText, Briefcase, User, Bot, Loader2 } from 'lucide-react';
import { startInterview, sendMessage } from './api/api';

function App() {
  // State: 'setup' | 'chat'
  const [view, setView] = useState('setup');

  // Data
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState('');
  const [sessionId, setSessionId] = useState(null);

  // Chat History
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  // Auto-scroll to bottom
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // --- HANDLERS ---

  const handleStart = async () => {
    if (!file || !jd) return alert("Please upload a resume and enter a JD.");

    setLoading(true);
    try {
      const data = await startInterview(file, jd);
      setSessionId(data.session_id);

      // Add AI's first message
      setMessages([{ sender: 'ai', text: data.message }]);
      setView('chat');
    } catch (error) {
      console.error(error);
      alert("Failed to start interview.");
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = input;
    setInput('');

    // Add User Message immediately
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const data = await sendMessage(sessionId, userMsg);
      // Add AI Response
      setMessages(prev => [...prev, { sender: 'ai', text: data.message }]);
    } catch (error) {
      console.error(error);
      alert("Failed to send message.");
    } finally {
      setLoading(false);
    }
  };

  // --- RENDER ---

  return (
    <div className="min-h-screen flex items-center justify-center p-4 font-sans text-slate-800">

      {/* Container */}
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-xl overflow-hidden min-h-[600px] flex flex-col">

        {/* Header */}
        <header className="bg-indigo-600 p-6 text-white flex items-center gap-3">
          <Bot size={32} />
          <div>
            <h1 className="text-xl font-bold">MockMate AI</h1>
            <p className="text-indigo-200 text-sm">Your technical interview partner</p>
          </div>
        </header>

        {/* VIEW 1: SETUP */}
        {view === 'setup' && (
          <div className="flex-1 p-8 flex flex-col gap-6 justify-center max-w-lg mx-auto w-full">

            <div className="space-y-2">
              <label className="font-semibold flex items-center gap-2">
                <FileText size={18} /> Upload Resume (PDF)
              </label>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-sm text-slate-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-indigo-50 file:text-indigo-700
                  hover:file:bg-indigo-100"
              />
            </div>

            <div className="space-y-2">
              <label className="font-semibold flex items-center gap-2">
                <Briefcase size={18} /> Job Description
              </label>
              <textarea
                value={jd}
                onChange={(e) => setJd(e.target.value)}
                placeholder="Paste the Job Description here..."
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none h-32 resize-none"
              />
            </div>

            <button
              onClick={handleStart}
              disabled={loading}
              className="bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:opacity-50 flex justify-center items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin" /> : "Start Interview"}
            </button>
          </div>
        )}

        {/* VIEW 2: CHAT */}
        {view === 'chat' && (
          <div className="flex-1 flex flex-col">

            {/* Messages Area */}
            <div className="flex-1 p-6 overflow-y-auto bg-slate-50 space-y-4 max-h-[500px]">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] p-4 rounded-xl shadow-sm whitespace-pre-wrap ${msg.sender === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-none'
                      : 'bg-white border text-slate-700 rounded-bl-none'
                    }`}>
                    {msg.text}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white border p-4 rounded-xl rounded-bl-none shadow-sm flex items-center gap-2 text-slate-500">
                    <Loader2 size={16} className="animate-spin" /> Thinking...
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t flex gap-3">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your answer..."
                className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="bg-indigo-600 text-white p-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                <Send size={20} />
              </button>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;