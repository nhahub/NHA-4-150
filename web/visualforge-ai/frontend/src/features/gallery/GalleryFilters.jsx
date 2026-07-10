import { Search } from "lucide-react";

import Input from "../../components/ui/Input.jsx";
import Select from "../../components/ui/Select.jsx";

export default function GalleryFilters({ filters, setFilters }) {
  const update = (key, value) => setFilters((current) => ({ ...current, [key]: value }));

  return (
    <div className="grid gap-3 rounded-lg border border-white/10 bg-white/[0.04] p-4 lg:grid-cols-[1fr_180px_190px_160px]">
      <label className="relative block">
        <Search
          size={17}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-forge-muted"
        />
        <Input
          value={filters.search}
          onChange={(event) => update("search", event.target.value)}
          placeholder="Search by prompt"
          className="pl-10"
        />
      </label>
      <Select value={filters.mode} onChange={(event) => update("mode", event.target.value)}>
        <option value="all">All modes</option>
        <option value="text_to_image">Text-to-Image</option>
        <option value="image_to_image">Image-to-Image</option>
        <option value="inpainting">Inpainting</option>
      </Select>
      <Select value={filters.domain} onChange={(event) => update("domain", event.target.value)}>
        <option value="all">All domains</option>
        <option value="base">General / Base</option>
        <option value="product_ads">Product Ads</option>
        <option value="egyptian_cultural">Egyptian Cultural</option>
      </Select>
      <Select value={filters.sort} onChange={(event) => update("sort", event.target.value)}>
        <option value="newest">Newest</option>
        <option value="oldest">Oldest</option>
      </Select>
    </div>
  );
}
