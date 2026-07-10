import { X } from "lucide-react";

import Button from "./Button.jsx";

export default function Modal({ open, title, children, onClose, size = "max-w-4xl" }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 py-8">
      <div className={`glass-card max-h-[90vh] w-full ${size} overflow-hidden rounded-lg`}>
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
          <h2 className="text-lg font-semibold text-forge-text">{title}</h2>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close modal">
            <X size={18} />
          </Button>
        </div>
        <div className="max-h-[calc(90vh-72px)] overflow-y-auto p-5">{children}</div>
      </div>
    </div>
  );
}
