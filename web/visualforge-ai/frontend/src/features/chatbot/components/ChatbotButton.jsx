import { MessageCircle } from "lucide-react";
import { useState } from "react";

import Logo2 from "../../../assets/Logo2.png";
import ChatbotPanel from "./ChatbotPanel.jsx";

export default function ChatbotButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="focus-ring fixed bottom-5 right-5 z-30 grid h-14 w-14 place-items-center rounded-full border border-forge-primary/40 bg-forge-panel shadow-glow transition hover:-translate-y-0.5 hover:border-forge-primary"
        aria-label="Open VisualForge Assistant"
        title="VisualForge Assistant"
      >
        <img src={Logo2} alt="" className="h-8 w-8 object-contain" />
        <MessageCircle size={16} className="absolute -right-1 -top-1 rounded-full bg-forge-primary p-0.5 text-slate-950" />
      </button>
      <ChatbotPanel open={open} onClose={() => setOpen(false)} />
    </>
  );
}
