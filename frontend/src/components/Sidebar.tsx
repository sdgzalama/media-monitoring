import { Link, useLocation } from "react-router-dom";
import { FiHome, FiDatabase, FiLayers } from "react-icons/fi";

export default function Sidebar() {
  const { pathname } = useLocation();

  const menu = [
    { label: "Dashboard", icon: <FiHome />, path: "/" },
    { label: "Projects", icon: <FiLayers />, path: "/projects" },
    { label: "Media Items", icon: <FiDatabase />, path: "/media" }
  ];

  return (
    <div
      style={{
        width: "240px",
        height: "100vh",
        background: "#6E3CBC",
        color: "white",
        display: "flex",
        flexDirection: "column",
        padding: "20px 0",
        position: "fixed",
        left: 0,
        top: 0,
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: "30px", fontSize: "22px" }}>
        🟣 HAMASA
      </h2>

      {menu.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          style={{
            textDecoration: "none",
            color: "white",
          }}
        >
          <div
            style={{
              padding: "12px 20px",
              display: "flex",
              alignItems: "center",
              gap: "10px",
              background: pathname === item.path ? "#512E89" : "transparent",
              cursor: "pointer",
              fontSize: "16px",
            }}
          >
            {item.icon}
            {item.label}
          </div>
        </Link>
      ))}
    </div>
  );
}
