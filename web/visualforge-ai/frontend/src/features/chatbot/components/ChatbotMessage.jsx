export default function ChatbotMessage({ message }) {
  const isAssistant = message.sender === "assistant";
  return (
    <div className={`flex ${isAssistant ? "justify-start" : "justify-end"}`}>
      <div
        className={`max-w-[82%] rounded-lg px-3 py-2 text-sm leading-6 ${
          isAssistant
            ? "border border-white/10 bg-white/[0.06] text-forge-text"
            : "bg-forge-primary text-slate-950"
        }`}
      >
        {message.text}
      </div>
    </div>
  );
}
