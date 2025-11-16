import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [sources, setSources] = useState<any[]>([]);
  const [loadingProjectId, setLoadingProjectId] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  // Load all projects
  const loadProjects = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/projects");
      const json = await res.json();
      setProjects(json);
    } catch (err) {
      console.error("Failed to load projects:", err);
    }
  };

  // Load all media sources
  const loadSources = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/media-sources/");
      const json = await res.json();
      setSources(json);
    } catch (err) {
      console.error("Failed to load sources:", err);
    }
  };

  useEffect(() => {
    loadProjects();
    loadSources();
  }, []);

  // Auto clear messages
  useEffect(() => {
    if (message) {
      const t = setTimeout(() => setMessage(""), 3000);
      return () => clearTimeout(t);
    }
  }, [message]);

  // SCRAPER ACTION
  const scrapeSource = async (projectId: string, sourceId: string) => {
    if (!sourceId) return; // ignore empty option

    setLoadingProjectId(projectId);
    setMessage("Scraping… please wait");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/scrape/rss?project_id=${projectId}&source_id=${sourceId}`,
        { method: "POST" }
      );

      const json = await res.json().catch(() => null);

      if (res.ok) {
        setMessage("✅ Scraping completed successfully!");
      } else {
        setMessage(`❌ Scraping failed: ${json?.detail || "Unknown error"}`);
      }
    } catch (err) {
      setMessage("❌ Network error while scraping.");
    }

    setLoadingProjectId(null);
  };

  return (
    <MainLayout>
      <h1 style={{ fontSize: "28px", fontWeight: "bold", marginBottom: "20px" }}>
        Projects
      </h1>

      {message && (
        <div
          style={{
            padding: "10px",
            background: "#f0f0f0",
            borderRadius: "6px",
            marginBottom: "10px",
            fontWeight: 500,
          }}
        >
          {message}
        </div>
      )}

      <table
        style={{
          width: "100%",
          marginTop: "20px",
          borderCollapse: "collapse",
          background: "white",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <thead>
          <tr style={{ background: "#f3f3f3" }}>
            <th style={{ padding: "12px", textAlign: "left" }}>Project Name</th>
            <th style={{ padding: "12px", textAlign: "left" }}>Client</th>
            <th style={{ padding: "12px", textAlign: "left" }}>Themes</th>
            <th style={{ padding: "12px", textAlign: "left" }}>Scrape</th>
            <th style={{ padding: "12px", textAlign: "left" }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {projects.length === 0 ? (
            <tr>
              <td style={{ padding: "15px" }} colSpan={4}>
                No projects found.
              </td>
            </tr>
          ) : (
            projects.map((p: any) => (
              <tr key={p.id} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "12px" }}>{p.name}</td>
                <td style={{ padding: "12px" }}>{p.client_name}</td>
                {/* THEMATIC AREAS */}
                <td style={{ padding: "12px" }}>
                  {p.thematic_areas.length === 0 ? (
                    <span style={{ opacity: 0.6 }}>No themes</span>
                  ) : (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                      {p.thematic_areas.map((t: string, index: number) => (
                        <span
                          key={index}
                          style={{
                            background: "#EDE9FE",
                            color: "#5B21B6",
                            padding: "4px 8px",
                            borderRadius: "6px",
                            fontSize: "12px",
                            fontWeight: 600,
                          }}
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                </td>


                <td style={{ padding: "12px" }}>
                  <select
                    style={{
                      padding: "6px",
                      borderRadius: "6px",
                      marginRight: "10px",
                    }}
                    onChange={(e) => {
                      if (!e.target.value) return;
                      const ok = confirm(`Scrape source for project "${p.name}"?`);
                      if (ok) scrapeSource(p.id, e.target.value);
                    }}
                    disabled={loadingProjectId === p.id}
                  >
                    <option value="">Scrape source...</option>
                    {sources.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>

                  {loadingProjectId === p.id && (
                    <span style={{ color: "#6d28d9", fontWeight: "bold" }}>
                      ⏳ Scraping…
                    </span>
                  )}
                </td>

                <td style={{ padding: "12px" }}>
                <Link
                to={`/analytics/${p.id}`}
                style={{
                  display: "inline-block",
                  background: "#6D28D9",
                  color: "white",
                  padding: "6px 10px",
                  borderRadius: "6px",
                  fontSize: "13px",
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                }}
              >
                View
              </Link>

                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </MainLayout>
  );
}
