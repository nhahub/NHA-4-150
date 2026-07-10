import Badge from "../../components/ui/Badge.jsx";
import Card from "../../components/ui/Card.jsx";
import Logo2 from "../../assets/Logo2.png";

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export default function RecentOutputs({ items = [], loading }) {
  return (
    <Card className="min-h-[320px] p-5">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-forge-text">Recent Outputs</h2>
          <p className="text-sm text-forge-muted">Latest generated images</p>
        </div>
      </div>
      {items.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {items.map((item) => (
            <article
              key={item.id}
              className="grid grid-cols-[96px_1fr] gap-3 rounded-lg border border-white/10 bg-white/[0.04] p-3"
            >
              <img
                src={item.image_url}
                alt={item.prompt}
                className="h-24 w-24 rounded-md object-cover"
              />
              <div className="min-w-0">
                <div className="flex flex-wrap gap-2">
                  <Badge value={item.mode} />
                  <Badge value={item.domain} />
                </div>
                <p className="mt-2 line-clamp-2 text-sm text-forge-text">{item.prompt}</p>
                <p className="mt-2 text-xs text-forge-muted">{formatDate(item.created_at)}</p>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <div className="grid h-52 place-items-center rounded-lg border border-dashed border-white/[0.12] text-center">
          <div>
            <img src={Logo2} alt="" className="mx-auto h-10 w-10 object-contain opacity-70" />
            <p className="mt-3 text-sm text-forge-muted">
              {loading ? "Loading outputs" : "No outputs saved yet"}
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}
