import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

const COLORS = ["#4CAF50", "#F44336"];

function Dashboard({ results }) {
  if (!results || results.length === 0) return null;

  const selected = results.filter(r => r.decision === "SELECT").length;
  const rejected = results.filter(r => r.decision === "REJECT").length;
  const total = results.length;

  const data = [
    { name: "Selected", value: selected },
    { name: "Rejected", value: rejected },
  ];

  return (
    <div style={{ marginTop: "40px" }}>
      <h3>📊 Hiring Dashboard</h3>

      <p><strong>Total Candidates:</strong> {total}</p>
      <p><strong>Selected:</strong> {selected}</p>
      <p><strong>Rejected:</strong> {rejected}</p>

      <PieChart width={400} height={300}>
        <Pie
          data={data}
          cx={200}
          cy={150}
          outerRadius={100}
          dataKey="value"
          label
        >
          {data.map((entry, index) => (
            <Cell key={index} fill={COLORS[index]} />
          ))}
        </Pie>

        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}

export default Dashboard;
