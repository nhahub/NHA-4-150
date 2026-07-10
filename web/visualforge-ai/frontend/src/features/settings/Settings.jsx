import { Activity, CheckCircle2, Database, FolderOpen, Server, XCircle } from "lucide-react";
import { useEffect, useState } from "react";

import Badge from "../../components/ui/Badge.jsx";
import Card from "../../components/ui/Card.jsx";
import LoadingSpinner from "../../components/ui/LoadingSpinner.jsx";
import apiClient from "../../services/apiClient.js";

function StatusCard({ icon: Icon, label, status, detail }) {
  const ready = status === "ready";
  return (
    <Card className="p-5">
      <div className="flex items-start gap-4">
        <span
          className={`grid h-11 w-11 shrink-0 place-items-center rounded-md ${
            ready ? "bg-forge-success/[0.12] text-emerald-200" : "bg-forge-error/[0.12] text-red-200"
          }`}
        >
          <Icon size={21} />
        </span>
        <div className="min-w-0">
          <p className="text-sm text-forge-muted">{label}</p>
          <div className="mt-2 flex items-center gap-2">
            {ready ? <CheckCircle2 size={17} /> : <XCircle size={17} />}
            <span className="font-semibold text-forge-text">{status || "unknown"}</span>
          </div>
          {detail && <p className="mt-2 break-words text-sm text-forge-muted">{detail}</p>}
        </div>
      </div>
    </Card>
  );
}

export default function Settings() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError("");
      try {
        const { data } = await apiClient.get("/health");
        if (active) setHealth(data);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <Card className="mx-auto grid min-h-72 max-w-7xl place-items-center p-5">
        <LoadingSpinner label="Checking API status" />
      </Card>
    );
  }

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-5">
      {error && (
        <div className="rounded-lg border border-forge-error/30 bg-forge-error/[0.12] p-4 text-sm text-red-100">
          {error}
        </div>
      )}

      <section className="grid gap-4 md:grid-cols-3">
        <StatusCard
          icon={Server}
          label="Backend Health"
          status={health?.backend?.status}
          detail="FastAPI application"
        />
        <StatusCard
          icon={Database}
          label="Database Status"
          status={health?.database?.status}
          detail={health?.database?.error}
        />
        <StatusCard
          icon={Activity}
          label="AI Engine Status"
          status={health?.ai?.status}
          detail={health?.ai?.error || health?.ai?.device}
        />
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <Card className="p-5">
          <h2 className="text-lg font-semibold text-forge-text">Available Modes</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {(health?.available_modes || []).map((mode) => (
              <Badge key={mode.value} value={mode.value}>
                {mode.label}
              </Badge>
            ))}
          </div>
        </Card>
        <Card className="p-5">
          <h2 className="text-lg font-semibold text-forge-text">Available Domains</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {(health?.available_domains || []).map((domain) => (
              <Badge key={domain.value} value={domain.value}>
                {domain.label}
              </Badge>
            ))}
          </div>
        </Card>
      </section>

      <Card className="p-5">
        <div className="mb-4 flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-md bg-forge-primary/[0.12] text-forge-primary">
            <FolderOpen size={20} />
          </span>
          <div>
            <h2 className="text-lg font-semibold text-forge-text">Output Directory Info</h2>
          </div>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
            <p className="text-sm text-forge-muted">Outputs Directory</p>
            <p className="mt-2 break-words text-sm font-semibold text-forge-text">
              {health?.storage?.outputs_dir}
            </p>
          </div>
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
            <p className="text-sm text-forge-muted">Uploads Directory</p>
            <p className="mt-2 break-words text-sm font-semibold text-forge-text">
              {health?.storage?.uploads_dir}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
