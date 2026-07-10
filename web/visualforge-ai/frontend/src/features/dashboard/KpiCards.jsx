import { Brush, Images, Layers3, WandSparkles } from "lucide-react";

import Card from "../../components/ui/Card.jsx";

const cards = [
  {
    label: "Total Generations",
    key: "total_generations",
    icon: Images,
    tone: "text-forge-primary bg-forge-primary/[0.12]",
  },
  {
    label: "Text-to-Image Count",
    key: "text_to_image_count",
    icon: WandSparkles,
    tone: "text-sky-200 bg-sky-400/[0.12]",
  },
  {
    label: "Image-to-Image Count",
    key: "image_to_image_count",
    icon: Layers3,
    tone: "text-violet-200 bg-violet-400/[0.12]",
  },
  {
    label: "Inpainting Count",
    key: "inpainting_count",
    icon: Brush,
    tone: "text-emerald-200 bg-emerald-400/[0.12]",
  },
];

export default function KpiCards({ summary, loading }) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map(({ label, key, icon: Icon, tone }) => (
        <Card key={key} className="p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm text-forge-muted">{label}</p>
              <p className="mt-3 text-3xl font-semibold text-forge-text">
                {loading ? "--" : summary[key] ?? 0}
              </p>
            </div>
            <span className={`grid h-11 w-11 place-items-center rounded-md ${tone}`}>
              <Icon size={21} />
            </span>
          </div>
        </Card>
      ))}
    </section>
  );
}
