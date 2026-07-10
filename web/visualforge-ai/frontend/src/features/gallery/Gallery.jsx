import { useEffect, useState } from "react";

import Card from "../../components/ui/Card.jsx";
import LoadingSpinner from "../../components/ui/LoadingSpinner.jsx";
import { generationApi } from "../../services/generationApi.js";
import GalleryFilters from "./GalleryFilters.jsx";
import ImageCard from "./ImageCard.jsx";
import OutputDetailsModal from "./OutputDetailsModal.jsx";

const initialFilters = {
  search: "",
  mode: "all",
  domain: "all",
  sort: "newest",
};

export default function Gallery() {
  const [filters, setFilters] = useState(initialFilters);
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError("");
      try {
        const data = await generationApi.list(filters);
        if (active) setItems(data);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }

    const handle = setTimeout(load, 220);
    return () => {
      active = false;
      clearTimeout(handle);
    };
  }, [filters]);

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-5">
      <Card className="p-5">
        <div className="mb-5 flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-forge-text">Gallery / History</h2>
          </div>
          <p className="text-sm text-forge-muted">{items.length} records</p>
        </div>
        <GalleryFilters filters={filters} setFilters={setFilters} />
      </Card>

      {error && (
        <div className="rounded-lg border border-forge-error/30 bg-forge-error/[0.12] p-4 text-sm text-red-100">
          {error}
        </div>
      )}

      {loading ? (
        <Card className="grid min-h-72 place-items-center p-5">
          <LoadingSpinner label="Loading gallery" />
        </Card>
      ) : items.length > 0 ? (
        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
          {items.map((item) => (
            <ImageCard key={item.id} item={item} onView={setSelected} />
          ))}
        </section>
      ) : (
        <Card className="grid min-h-72 place-items-center p-5 text-sm text-forge-muted">
          No gallery items found
        </Card>
      )}

      <OutputDetailsModal item={selected} onClose={() => setSelected(null)} />
    </div>
  );
}
