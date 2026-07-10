const palette = {
  text_to_image: "border-sky-400/[0.35] bg-sky-400/[0.12] text-sky-100",
  image_to_image: "border-violet-400/[0.35] bg-violet-400/[0.12] text-violet-100",
  inpainting: "border-emerald-400/[0.35] bg-emerald-400/[0.12] text-emerald-100",
  base: "border-slate-300/25 bg-white/[0.08] text-slate-100",
  product_ads: "border-amber-400/[0.35] bg-amber-400/[0.12] text-amber-100",
  egyptian_cultural: "border-fuchsia-400/[0.35] bg-fuchsia-400/[0.12] text-fuchsia-100",
  completed: "border-emerald-400/[0.35] bg-emerald-400/[0.12] text-emerald-100",
  failed: "border-red-400/[0.35] bg-red-400/[0.12] text-red-100",
};

const labels = {
  text_to_image: "Text-to-Image",
  image_to_image: "Image-to-Image",
  inpainting: "Inpainting",
  base: "General / Base",
  product_ads: "Product Ads",
  egyptian_cultural: "Egyptian Cultural",
};

export default function Badge({ value, children, className = "" }) {
  return (
    <span
      className={`inline-flex min-h-7 items-center rounded-md border px-2.5 py-1 text-xs font-semibold ${palette[value] || "border-white/[0.12] bg-white/[0.08] text-forge-muted"} ${className}`}
    >
      {children || labels[value] || value}
    </span>
  );
}
