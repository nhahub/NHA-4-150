import Input from "../../components/ui/Input.jsx";

function NumberField({ label, value, onChange, min, max, step = 1 }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-semibold text-forge-text">{label}</span>
      <Input
        type="number"
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </label>
  );
}

export default function SettingsPanel({ mode, settings, setSettings }) {
  const update = (key, value) => setSettings((current) => ({ ...current, [key]: value }));

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <NumberField label="Seed" value={settings.seed} onChange={(value) => update("seed", value)} />
      <NumberField
        label="Steps"
        value={settings.steps}
        min={1}
        max={80}
        onChange={(value) => update("steps", value)}
      />
      <NumberField
        label="Guidance Scale"
        value={settings.guidance_scale}
        min={1}
        max={20}
        step={0.1}
        onChange={(value) => update("guidance_scale", value)}
      />
      {mode !== "text_to_image" && (
        <NumberField
          label="Strength"
          value={settings.strength}
          min={0}
          max={1}
          step={0.01}
          onChange={(value) => update("strength", value)}
        />
      )}
      <NumberField
        label="Width"
        value={settings.width}
        min={256}
        max={1536}
        step={64}
        onChange={(value) => update("width", value)}
      />
      <NumberField
        label="Height"
        value={settings.height}
        min={256}
        max={1536}
        step={64}
        onChange={(value) => update("height", value)}
      />
    </div>
  );
}
