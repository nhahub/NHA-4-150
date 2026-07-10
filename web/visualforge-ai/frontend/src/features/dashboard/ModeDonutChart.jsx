import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import Card from "../../components/ui/Card.jsx";

const colors = ["#38BDF8", "#8B5CF6", "#22C55E"];

export default function ModeDonutChart({ data = [] }) {
  const hasData = data.some((item) => item.count > 0);

  return (
    <Card className="min-h-[330px] p-5">
      <h2 className="text-lg font-semibold text-forge-text">Mode Distribution</h2>
      <p className="text-sm text-forge-muted">Usage by generation mode</p>
      {hasData ? (
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_150px] xl:grid-cols-1">
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  dataKey="count"
                  nameKey="label"
                  innerRadius={58}
                  outerRadius={88}
                  paddingAngle={4}
                >
                  {data.map((entry, index) => (
                    <Cell key={entry.mode} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "#111827",
                    border: "1px solid rgba(255,255,255,0.12)",
                    borderRadius: 8,
                    color: "#F8FAFC",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col justify-center gap-3">
            {data.map((item, index) => (
              <div key={item.mode} className="flex items-center justify-between gap-3 text-sm">
                <span className="flex items-center gap-2 text-forge-muted">
                  <span
                    className="h-2.5 w-2.5 rounded-sm"
                    style={{ backgroundColor: colors[index % colors.length] }}
                  />
                  {item.label}
                </span>
                <span className="font-semibold text-forge-text">{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="mt-6 grid h-56 place-items-center rounded-lg border border-dashed border-white/[0.12] text-sm text-forge-muted">
          No mode data yet
        </div>
      )}
    </Card>
  );
}
