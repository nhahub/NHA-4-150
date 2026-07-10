import { Send, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import Button from "../../../components/ui/Button.jsx";
import Input from "../../../components/ui/Input.jsx";
import Logo2 from "../../../assets/Logo2.png";
import { chatbotApi } from "../services/chatbotApi.js";
import ChatbotMessage from "./ChatbotMessage.jsx";

const initialMessage = {
  sender: "assistant",
  text: "Hi, I am VisualForge Assistant. I can help you understand the studio tools.",
};

function rowsToMessages(rows) {
  if (!rows?.length) return [initialMessage];
  return [
    initialMessage,
    ...rows.flatMap((row) => [
      { sender: "user", text: row.message },
      { sender: "assistant", text: row.response },
    ]),
  ];
}

export default function ChatbotPanel({ open, onClose }) {
  const [messages, setMessages] = useState([initialMessage]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    let active = true;
    chatbotApi
      .history()
      .then((rows) => {
        if (active) setMessages(rowsToMessages(rows));
      })
      .catch(() => {
        if (active) setMessages([initialMessage]);
      });
    return () => {
      active = false;
    };
  }, [open]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  async function send(event) {
    event.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((current) => [...current, { sender: "user", text }]);
    setLoading(true);
    try {
      const result = await chatbotApi.sendMessage(text);
      setMessages((current) => [
        ...current,
        { sender: "assistant", text: result.response },
      ]);
    } catch (err) {
      setMessages((current) => [
        ...current,
        { sender: "assistant", text: err.message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function clear() {
    await chatbotApi.clear().catch(() => null);
    setMessages([initialMessage]);
  }

  return (
    <aside
      className={`fixed bottom-5 right-5 z-40 flex h-[min(680px,calc(100vh-40px))] w-[min(420px,calc(100vw-32px))] flex-col overflow-hidden rounded-lg border border-white/[0.12] bg-forge-panel/95 shadow-2xl backdrop-blur-xl transition ${
        open ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0"
      }`}
    >
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="flex items-center gap-3">
          <img src={Logo2} alt="" className="h-9 w-9 object-contain" />
          <div>
            <h2 className="text-base font-semibold text-forge-text">VisualForge Assistant</h2>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" onClick={clear} aria-label="Clear chat" title="Clear">
            <Trash2 size={17} />
          </Button>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close chatbot" title="Close">
            <X size={18} />
          </Button>
        </div>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <ChatbotMessage key={`${message.sender}-${index}`} message={message} />
        ))}
        {loading && <ChatbotMessage message={{ sender: "assistant", text: "Thinking" }} />}
        <div ref={endRef} />
      </div>

      <form onSubmit={send} className="flex gap-2 border-t border-white/10 p-3">
        <Input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask VisualForge Assistant"
        />
        <Button type="submit" size="icon" aria-label="Send message" disabled={loading}>
          <Send size={18} />
        </Button>
      </form>
    </aside>
  );
}
