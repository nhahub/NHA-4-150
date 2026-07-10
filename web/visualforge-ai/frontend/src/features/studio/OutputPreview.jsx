import { Download, Image } from "lucide-react";

import Badge from "../../components/ui/Badge.jsx";
import Button from "../../components/ui/Button.jsx";
import Card from "../../components/ui/Card.jsx";
import LoadingSpinner from "../../components/ui/LoadingSpinner.jsx";

export default function OutputPreview({ output, loading }) {
  return (
    <Card className="flex min-h-[520px] flex-col p-5">
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-forge-text">Output Preview</h2>
        </div>
        {output?.image_url && (
          <a href={output.image_url} download target="_blank" rel="noreferrer">
            <Button variant="secondary" size="sm">
              <Download size={16} />
              Download
            </Button>
          </a>
        )}
      </div>

      <div className="grid flex-1 place-items-center overflow-hidden rounded-lg border border-white/10 bg-black/20">
        {loading ? (
          <LoadingSpinner label="Generating output" />
        ) : output?.image_url ? (
          <img src={output.image_url} alt="Generated output" className="h-full w-full object-contain" />
        ) : (
          <div className="flex flex-col items-center gap-3 text-forge-muted">
            <span className="grid h-12 w-12 place-items-center rounded-md bg-white/[0.08]">
              <Image size={24} />
            </span>
            <span className="text-sm">No output selected</span>
          </div>
        )}
      </div>

      {output?.metadata && (
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge value={output.metadata.mode} />
          <Badge value={output.metadata.domain} />
          <Badge value={output.metadata.status} />
        </div>
      )}
    </Card>
  );
}
