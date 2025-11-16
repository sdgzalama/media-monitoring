import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";

export default function MediaItems() {
  const [items, setItems] = useState<any[]>([]);
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  const loadItems = async () => {
    const res = await fetch("http://127.0.0.1:8000/media/");
    const json = await res.json();
    setItems(json);
  };

  useEffect(() => {
    loadItems();
  }, []);

  const analyzeItem = async (mediaId: string) => {
    setLoadingId(mediaId);

    const res = await fetch(
      `http://127.0.0.1:8000/process/media-item/${mediaId}`,
      { method: "POST" }
    );

    if (res.ok) {
      setMessage("✔ Item analyzed successfully");
      loadItems();
    } else {
      setMessage("❌ Failed to analyze");
    }

    setLoadingId(null);
  };

  const analyzeAll = async () => {
    setMessage("⏳ Processing ALL items…");

    const res = await fetch("http://127.0.0.1:8000/media/process/all", {
      method: "POST",
    });

    const json = await res.json();
    setMessage(`✔ Queued ${json.total} items`);
    loadItems();
  };

  return (
    <MainLayout>
      <h1 style={{ fontSize: "28px", fontWeight: "bold" }}>Media Items</h1>

      {message && (
        <div
          style={{
            background: "#eee",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "6px",
          }}
        >
          {message}
        </div>
      )}

      <button
        onClick={analyzeAll}
        style={{
          background: "#6D28D9",
          color: "white",
          padding: "10px 15px",
          borderRadius: "8px",
          border: "none",
          marginBottom: "15px",
          cursor: "pointer",
        }}
      >
        ⚡ Analyze ALL
      </button>

      <table
  style={{
    width: "100%",
    background: "white",
    borderRadius: "10px",
    overflow: "hidden",
    borderCollapse: "collapse",
  }}
>
  <thead>
    <tr>
      <th style={{ padding: "12px", textAlign: "left" }}>Title</th>
      <th style={{ padding: "12px", textAlign: "left" }}>Source</th>
      <th style={{ padding: "12px", textAlign: "left" }}>Url</th>
      <th style={{ padding: "12px", textAlign: "left" }}>scraped_at</th>

      <th style={{ padding: "12px", textAlign: "left" }}>Status</th>
      <th style={{ padding: "12px", textAlign: "left" }}>Action</th>
    </tr>
  </thead>

  <tbody>
    {items.map((item) => (
      <tr key={item.id} style={{ borderBottom: "1px solid #eee" }}>
        <td style={td}>{item.raw_title}</td>
        <td style={td}>{item.source_name}</td>
        <td style={td}>{item.url}</td>
        <td style={td}>{item.scraped_at}</td>
        <td style={td}>
          {item.analysis_status === "extracted"
            ? "✔ Extracted"
            : "⏳ Raw"}
        </td>
        <td style={td}>
          <button
            onClick={() => analyzeItem(item.id)}
            disabled={loadingId === item.id}
            style={{
              background: "#6D28D9",
              color: "white",
              padding: "6px 8px",
              borderRadius: "6px",
              border: "none",
              cursor: "pointer",
            }}
          >
            {loadingId === item.id ? "Analyzing…" : "Analyze"}
          </button>
        </td>
      </tr>
    ))}
  </tbody>
</table>

    </MainLayout>
  );
}

// const th = { padding: "10px", textAlign: "left" };
const td = { padding: "10px" };
