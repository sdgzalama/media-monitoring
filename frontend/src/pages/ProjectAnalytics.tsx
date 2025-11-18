import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

export default function ProjectAnalytics() {
  const { id } = useParams(); // project_id from URL

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // -----------------------
  // LOAD PROJECT DASHBOARD
  // -----------------------
  const loadAnalytics = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/project/${id}/dashboard`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    } catch (err) {
      console.error("Analytics Load Error:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();

    // auto refresh every 10 seconds
    const interval = setInterval(loadAnalytics, 10000);

    return () => clearInterval(interval);
  }, [id]);

  if (loading || !data) {
    return (
      <MainLayout>
        <h1 style={{ fontSize: "24px", fontWeight: "bold" }}>Loading Project Analytics...</h1>
      </MainLayout>
    );
  }

  const { project, stats, global_stats, sources, themes, industry_names, tactics, stakeholders, geographical_focus, outcomes } = data;

  return (
    <MainLayout>
      <div
  style={{
    display: "flex",
    alignItems: "center",
    gap: "15px",
    padding: "20px 25px",
    borderRadius: "14px",
    background: "white",
    border: "1px solid #DDD",
    marginBottom: "28px",
  }}
>
  <div
    style={{
      width: "50px",
      height: "50px",
      borderRadius: "12px",
      background: "#6D28D9",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "white",
      fontSize: "24px",
      fontWeight: 700
    }}
  >
    📊
  </div>

  <div>
    <h1 style={{ margin: 0, fontSize: "24px", fontWeight: 700 }}>
     Project Title:  {project.title}
    </h1>
    <p style={{ margin: 0, fontSize: "15px", color: "#6B7280" }}>
      Client: {project.client_name || "Not specified"}
    </p>
  </div>
</div>



      {/* ===================== SECTION 1: STATS ===================== */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "20px",
          marginBottom: "40px",
        }}
      >
        <StatCard title="Total Media Items" value={stats.total_items} globalValue={global_stats?.total_items} />
        <StatCard title="Analysed" value={stats.extracted_items} globalValue={global_stats?.extracted_items} />
        <StatCard title="Pending AI" value={stats.awaiting_items} globalValue={global_stats?.awaiting_items} />
      </div>

      {/* ===================== SECTION 2: CHARTS ===================== */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "25px",
          marginBottom: "40px",
        }}
      >
        {/* Pie — by Sources */}
        <ChartBox title="Media Distribution by Source">
          <Pie
            data={{
              labels: sources.map((s: any) => s.name),
              datasets: [
                {
                  data: sources.map((s: any) => s.count),
                  backgroundColor: ["#9333ea", "#a855f7", "#c084fc", "#e879f9"],
                },
              ],
            }}
          />
        </ChartBox>

        {/* Bar — by Thematic Areas */}
        <ChartBox title="Thematic Area Distribution">
          <Bar
            data={{
              labels: themes.map((t: any) => t.name),
              datasets: [
                {
                  label: "Mentions",
                  data: themes.map((t: any) => t.count),
                  backgroundColor: "#a855f7",
                },
              ],
            }}
          />
        </ChartBox>
      </div>

      {/* ===================== SECTION 3: TABLES ===================== */}

      <DataTable title="Industry Names" rows={industry_names} field="industry_name" />
      <DataTable title="Industry Tactics" rows={tactics} field="industry_tactic" />
      <DataTable title="Geographical Focus" rows={geographical_focus} field="geographical_focus" />
      <DataTable title="Outcome / Impact" rows={outcomes} field="outcome_impact" />

      {/* Stakeholders list */}
      <div style={{ background: "white", padding: "20px", borderRadius: "12px", marginTop: "25px" }}>
        <h3 style={{ marginBottom: "10px" }}>Stakeholders Frequency</h3>

        {Object.keys(stakeholders).length === 0 ? (
          <p>No stakeholders found.</p>
        ) : (
          <ul>
            {Object.entries(stakeholders).map(([name, count]: any) => (
              <li key={name}>
                <strong>{name}</strong>: {count}
              </li>
            ))}
          </ul>
        )}
      </div>
    </MainLayout>
  );
}

// ===================== COMPONENTS =====================

function StatCard({ title, value }: any) {
  return (
    <div
      style={{
        background: "#6d28d9",
        color: "white",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 3px 7px rgba(0,0,0,0.15)",
      }}
    >
      <h3>{title}</h3>
      <p style={{ fontSize: "32px", fontWeight: "bold" }}>{value}</p>
      {/** show shared/global dataset value for context */}
      <p style={{ fontSize: "12px", opacity: 0.9, marginTop: 6 }}>Shared dataset: { (arguments[0] as any).globalValue ?? '—' }</p>
    </div>
  );
}

function ChartBox({ title, children }: any) {
  return (
    <div style={{ background: "white", padding: "20px", borderRadius: "12px" }}>
      <h3>{title}</h3>
      {children}
    </div>
  );
}

function DataTable({ title, rows, field }: any) {
  return (
    <div style={{ background: "white", padding: "20px", borderRadius: "12px", marginTop: "25px" }}>
      <h3>{title}</h3>
      <table style={{ width: "100%", marginTop: "15px", borderCollapse: "collapse" }}>
        <tbody>
          {rows.length === 0 ? (
            <tr><td>No data.</td></tr>
          ) : (
            rows.map((r: any, index: number) => (
              <tr key={index} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "10px" }}>{r[field]}</td>
                <td style={{ padding: "10px" }}>{r.count}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
