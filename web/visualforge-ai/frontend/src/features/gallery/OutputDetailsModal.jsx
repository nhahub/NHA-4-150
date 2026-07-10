import { Download } from "lucide-react";

import Badge from "../../components/ui/Badge.jsx";
import Button from "../../components/ui/Button.jsx";
import Modal from "../../components/ui/Modal.jsx";

function Detail({ label, value }) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/[0.04] p-3">
      <p className="text-xs uppercase tracking-[0.12em] text-forge-muted">{label}</p>
      <p className="mt-2 break-words text-sm font-semibold text-forge-text">{value ?? "Not set"}</p>
    </div>
  );
}

export default function OutputDetailsModal({ item, onClose }) {
  return (
    <Modal open={Boolean(item)} title="Output Details" onClose={onClose} size="max-w-6xl">
      {item && (
        <div className="grid gap-5 lg:grid-cols-[1fr_390px]">
          <div className="overflow-hidden rounded-lg border border-white/10 bg-black/30">
            <img src={item.image_url} alt={item.prompt} className="max-h-[70vh] w-full object-contain" />
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex flex-wrap gap-2">
              <Badge value={item.mode} />
              <Badge value={item.domain} />
              <Badge value={item.status} />
            </div>
            <div>
              <p className="text-sm font-semibold text-forge-text">Prompt</p>
              <p className="mt-2 rounded-lg border border-white/10 bg-white/[0.04] p-3 text-sm leading-6 text-forge-muted">
                {item.prompt}
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <Detail label="Seed" value={item.seed} />
              <Detail label="Steps" value={item.steps} />
              <Detail label="Guidance" value={item.guidance_scale} />
              <Detail label="Strength" value={item.strength} />
              <Detail label="Width" value={item.width} />
              <Detail label="Height" value={item.height} />
            </div>
            <Detail label="Image Path" value={item.image_path} />
            {item.image_url && (
              <a href={item.image_url} download target="_blank" rel="noreferrer">
                <Button className="w-full">
                  <Download size={17} />
                  Download
                </Button>
              </a>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
}
