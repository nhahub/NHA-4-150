import { AlertCircle, Sparkles } from "lucide-react";
import { useMemo, useState } from "react";

import Button from "../../components/ui/Button.jsx";
import Card from "../../components/ui/Card.jsx";
import { generationApi } from "../../services/generationApi.js";
import DomainSelector from "./DomainSelector.jsx";
import ModeSelector from "./ModeSelector.jsx";
import OutputPreview from "./OutputPreview.jsx";
import PromptBox from "./PromptBox.jsx";
import SettingsPanel from "./SettingsPanel.jsx";
import UploadArea from "./UploadArea.jsx";

const initialSettings = {
  seed: 42,
  steps: 30,
  guidance_scale: 7.5,
  strength: 0.35,
  width: 1024,
  height: 1024,
};

export default function Studio() {
  const [mode, setMode] = useState("text_to_image");
  const [domain, setDomain] = useState("base");
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [mask, setMask] = useState(null);
  const [settings, setSettings] = useState(initialSettings);
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const requiresImage = mode === "image_to_image" || mode === "inpainting";
  const requiresMask = mode === "inpainting";

  const requestPayload = useMemo(
    () => ({
      prompt,
      domain,
      seed: settings.seed,
      steps: settings.steps,
      guidance_scale: settings.guidance_scale,
      strength: settings.strength,
      width: settings.width,
      height: settings.height,
      image,
      mask,
    }),
    [domain, image, mask, prompt, settings],
  );

  async function handleGenerate(event) {
    event.preventDefault();
    setError("");

    if (!prompt.trim()) {
      setError("Prompt is required.");
      return;
    }
    if (requiresImage && !image) {
      setError("Image upload is required for this mode.");
      return;
    }
    if (requiresMask && !mask) {
      setError("Mask upload is required for inpainting.");
      return;
    }

    setLoading(true);
    try {
      const result =
        mode === "text_to_image"
          ? await generationApi.textToImage(requestPayload)
          : mode === "image_to_image"
            ? await generationApi.imageToImage(requestPayload)
            : await generationApi.inpaint(requestPayload);
      setOutput(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleGenerate} className="mx-auto grid max-w-7xl gap-5 xl:grid-cols-[1fr_420px]">
      <div className="flex flex-col gap-5">
        <Card className="p-5">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-forge-text">Generation Mode</h2>
          </div>
          <ModeSelector value={mode} onChange={setMode} />
        </Card>

        <Card className="p-5">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-forge-text">Creative Domain</h2>
          </div>
          <DomainSelector value={domain} onChange={setDomain} />
        </Card>

        <Card className="p-5">
          <PromptBox value={prompt} onChange={setPrompt} />
        </Card>

        {requiresImage && (
          <Card className="grid gap-5 p-5 lg:grid-cols-2">
            <UploadArea label="Source Image" file={image} onChange={setImage} />
            {requiresMask && <UploadArea label="Mask Image" file={mask} onChange={setMask} />}
          </Card>
        )}

        <Card className="p-5">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-forge-text">Settings</h2>
          </div>
          <SettingsPanel mode={mode} settings={settings} setSettings={setSettings} />
        </Card>

        {error && (
          <div className="flex items-start gap-3 rounded-lg border border-forge-error/30 bg-forge-error/[0.12] p-4 text-sm text-red-100">
            <AlertCircle className="mt-0.5 shrink-0" size={18} />
            <span>{error}</span>
          </div>
        )}

        <div className="flex justify-end">
          <Button type="submit" size="lg" disabled={loading}>
            <Sparkles size={18} />
            {loading ? "Generating" : "Generate"}
          </Button>
        </div>
      </div>

      <OutputPreview output={output} loading={loading} />
    </form>
  );
}
