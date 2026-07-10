import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import Card from "../../components/ui/Card.jsx";

export default function DomainBarChart({ data = [] }) {
  const hasData = data.some((item) => item.count > 0);

  return (
    <Card className="min-h-[320px] p-5">
      <h2 className="text-lg font-semibold text-forge-text">Domain Usage</h2>
      <p className="text-sm text-forge-muted">Creative direction frequency</p>
      {hasData ? (
        <div className="mt-5 h-60">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
              <XAxis dataKey="label" stroke="#94A3B8" tickLine={false} axisLine={false} />
              <YAxis allowDecimals={false} stroke="#94A3B8" tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  background: "#111827",
                  border: "1px solid rgba(255,255,255,0.12)",
                  borderRadius: 8,
                  color: "#F8FAFC",
                }}
              />
              <Bar dataKey="count" fill="#8B5CF6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="mt-5 grid h-60 place-items-center rounded-lg border border-dashed border-white/[0.12] text-sm text-forge-muted">
          No domain data yet
        </div>
      )}
    </Card>
  );
}
