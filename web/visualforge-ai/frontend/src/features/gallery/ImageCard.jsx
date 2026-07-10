import { Download, Eye } from "lucide-react";

import Badge from "../../components/ui/Badge.jsx";
import Button from "../../components/ui/Button.jsx";

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(value));
}

export default function ImageCard({ item, onView }) {
  return (
    <article className="group overflow-hidden rounded-lg border border-white/10 bg-white/[0.05] transition hover:border-forge-primary/40 hover:bg-white/[0.075]">
      <div className="aspect-square overflow-hidden bg-black/30">
        {item.image_url ? (
          <img
            src={item.image_url}
            alt={item.prompt}
            className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]"
          />
        ) : (
          <div className="grid h-full place-items-center text-sm text-forge-muted">No image</div>
        )}
      </div>
      <div className="p-4">
        <div className="flex flex-wrap gap-2">
          <Badge value={item.mode} />
          <Badge value={item.domain} />
        </div>
        <p className="mt-3 line-clamp-2 min-h-10 text-sm text-forge-text">{item.prompt}</p>
        <p className="mt-2 text-xs text-forge-muted">{formatDate(item.created_at)}</p>
        <div className="mt-4 flex gap-2">
          <Button variant="secondary" size="sm" onClick={() => onView(item)}>
            <Eye size={15} />
            View
          </Button>
          {item.image_url && (
            <a
              href={item.image_url}
              download
              target="_blank"
              rel="noreferrer"
              className="inline-flex h-9 items-center justify-center gap-2 rounded-md border border-white/[0.12] bg-white/[0.08] px-3 text-sm font-semibold text-forge-text transition hover:bg-white/[0.12]"
            >
              <Download size={15} />
              Download
            </a>
          )}
        </div>
      </div>
    </article>
  );
}
