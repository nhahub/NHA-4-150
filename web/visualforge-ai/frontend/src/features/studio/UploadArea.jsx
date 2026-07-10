import { ImageUp, X } from "lucide-react";
import { useMemo, useRef } from "react";

import Button from "../../components/ui/Button.jsx";

export default function UploadArea({ label, file, onChange }) {
  const inputRef = useRef(null);
  const preview = useMemo(() => (file ? URL.createObjectURL(file) : ""), [file]);

  function handleDrop(event) {
    event.preventDefault();
    const nextFile = event.dataTransfer.files?.[0];
    if (nextFile) onChange(nextFile);
  }

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-semibold text-forge-text">{label}</span>
        {file && (
          <Button variant="ghost" size="sm" onClick={() => onChange(null)}>
            <X size={16} />
            Clear
          </Button>
        )}
      </div>
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
        className="focus-ring grid min-h-44 w-full place-items-center overflow-hidden rounded-lg border border-dashed border-white/[0.18] bg-white/[0.04] text-left transition hover:border-forge-primary/60"
      >
        {file ? (
          <img src={preview} alt={file.name} className="h-44 w-full object-cover" />
        ) : (
          <span className="flex flex-col items-center gap-3 text-sm text-forge-muted">
            <span className="grid h-11 w-11 place-items-center rounded-md bg-forge-primary/[0.12] text-forge-primary">
              <ImageUp size={22} />
            </span>
            Upload image
          </span>
        )}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(event) => onChange(event.target.files?.[0] || null)}
      />
    </div>
  );
}
