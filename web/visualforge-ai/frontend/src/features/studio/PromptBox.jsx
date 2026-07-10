import Input from "../../components/ui/Input.jsx";

export default function PromptBox({ value, onChange }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-semibold text-forge-text">Prompt</span>
      <Input
        as="textarea"
        rows={7}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Describe the image you want VisualForge AI to create"
        className="resize-none leading-6"
      />
    </label>
  );
}
