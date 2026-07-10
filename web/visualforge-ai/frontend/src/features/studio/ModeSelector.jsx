import { Brush, ImagePlus, WandSparkles } from "lucide-react";

const modes = [
  { value: "text_to_image", label: "Text-to-Image", icon: WandSparkles },
  { value: "image_to_image", label: "Image-to-Image", icon: ImagePlus },
  { value: "inpainting", label: "Inpainting", icon: Brush },
];

export default function ModeSelector({ value, onChange }) {
  return (
    <div className="grid gap-3 sm:grid-cols-3">
      {modes.map(({ value: modeValue, label, icon: Icon }) => {
        const selected = value === modeValue;
        return (
          <button
            key={modeValue}
            type="button"
            onClick={() => onChange(modeValue)}
            className={`focus-ring flex min-h-24 flex-col justify-between rounded-lg border p-4 text-left transition ${
              selected
                ? "border-forge-primary bg-forge-primary/[0.14] text-forge-text shadow-glow"
                : "border-white/[0.12] bg-white/[0.04] text-forge-muted hover:border-white/20 hover:text-forge-text"
            }`}
          >
            <Icon size={22} />
            <span className="text-sm font-semibold">{label}</span>
          </button>
        );
      })}
    </div>
  );
}
