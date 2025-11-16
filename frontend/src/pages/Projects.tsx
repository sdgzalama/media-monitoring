import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

export default function Projects() {
  const [projects, setProjects] = useState([]);

  // Load all projects from backend
  const loadProjects = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/projects");
      const json = await res.json();
      setProjects(json);
    } catch (err) {
      console.error("Failed to load projects:", err);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  return (
    <MainLayout>
      <h1 style={{ fontSize: "28px", fontWeight: "bold", marginBottom: "20px" }}>
        Projects
      </h1>

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
            <th style={{ padding: "12px", textAlign: "left" }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {projects.length === 0 ? (
            <tr>
              <td style={{ padding: "15px" }} colSpan={3}>
                No projects found.
              </td>
            </tr>
          ) : (
            projects.map((p: any) => (
              <tr key={p.id} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "12px" }}>{p.name}</td>
                <td style={{ padding: "12px" }}>{p.client_name}</td>

                <td style={{ padding: "12px" }}>
                  <Link
                    to={`/analytics/${p.id}`}
                    style={{
                      padding: "8px 16px",
                      background: "#6d28d9",
                      color: "white",
                      borderRadius: "6px",
                      textDecoration: "none",
                      fontSize: "14px",
                    }}
                  >
                    📊 View Analytics
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
