import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import Card from "../../components/ui/Card.jsx";

export default function GenerationLineChart({ data }) {
  const hasData = data?.some((item) => item.count > 0);

  return (
    <Card className="min-h-[330px] p-5">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-forge-text">Generations Over Time</h2>
          <p className="text-sm text-forge-muted">Daily output volume</p>
        </div>
      </div>
      {hasData ? (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="generationGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38BDF8" stopOpacity={0.45} />
                  <stop offset="95%" stopColor="#38BDF8" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
              <XAxis dataKey="date" stroke="#94A3B8" tickLine={false} axisLine={false} />
              <YAxis allowDecimals={false} stroke="#94A3B8" tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  background: "#111827",
                  border: "1px solid rgba(255,255,255,0.12)",
                  borderRadius: 8,
                  color: "#F8FAFC",
                }}
              />
              <Area
                type="monotone"
                dataKey="count"
                stroke="#38BDF8"
                strokeWidth={3}
                fill="url(#generationGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="grid h-64 place-items-center rounded-lg border border-dashed border-white/[0.12] text-sm text-forge-muted">
          No generation data yet
        </div>
      )}
    </Card>
  );
}
