import { useEffect, useState } from "react";

import { analyticsApi } from "../../services/analyticsApi.js";
import { generationApi } from "../../services/generationApi.js";
import DomainBarChart from "./DomainBarChart.jsx";
import GenerationLineChart from "./GenerationLineChart.jsx";
import KpiCards from "./KpiCards.jsx";
import ModeDonutChart from "./ModeDonutChart.jsx";
import RecentOutputs from "./RecentOutputs.jsx";

const emptySummary = {
  total_generations: 0,
  text_to_image_count: 0,
  image_to_image_count: 0,
  inpainting_count: 0,
  most_used_domain: null,
};

const emptyCharts = {
  generations_over_time: [],
  mode_distribution: [],
  domain_usage: [],
};

export default function Dashboard() {
  const [summary, setSummary] = useState(emptySummary);
  const [charts, setCharts] = useState(emptyCharts);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function loadDashboard() {
      setLoading(true);
      setError("");
      try {
        const [summaryData, chartData, recentData] = await Promise.all([
          analyticsApi.summary(),
          analyticsApi.charts(),
          generationApi.list({ sort: "newest" }),
        ]);
        if (!active) return;
        setSummary(summaryData);
        setCharts(chartData);
        setRecent(recentData.slice(0, 6));
      } catch (err) {
        if (!active) return;
        setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    loadDashboard();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-5">
      <section className="grid gap-5 lg:grid-cols-[1.45fr_0.55fr]">
        <div className="glass-card rounded-lg p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-forge-primary">
            VisualForge AI
          </p>
          <div className="mt-4 flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-3xl font-semibold text-forge-text md:text-4xl">
                AI Visual Content Studio
              </h2>
            </div>
            {error && (
              <div className="rounded-md border border-forge-warning/30 bg-forge-warning/10 px-3 py-2 text-sm text-amber-100">
                {error}
              </div>
            )}
          </div>
        </div>
        <div className="glass-card rounded-lg p-6">
          <p className="text-sm text-forge-muted">Most Used Domain</p>
          <p className="mt-3 text-2xl font-semibold text-forge-text">
            {summary.most_used_domain || "No data yet"}
          </p>
          <div className="mt-5 h-2 overflow-hidden rounded-md bg-white/[0.08]">
            <div className="h-full w-2/3 rounded-md bg-forge-primary" />
          </div>
        </div>
      </section>

      <KpiCards summary={summary} loading={loading} />

      <section className="grid gap-5 xl:grid-cols-[1.25fr_0.75fr]">
        <GenerationLineChart data={charts.generations_over_time} />
        <ModeDonutChart data={charts.mode_distribution} />
      </section>

      <section className="grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
        <DomainBarChart data={charts.domain_usage} />
        <RecentOutputs items={recent} loading={loading} />
      </section>
    </div>
  );
}
