// import Sidebar from "../components/Sidebar";
import Sidebar from "../components/sidebar";
import Topbar from "../components/Topbar";

export default function MainLayout({ children }: { children: any }) {
  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <Sidebar />
      <Topbar />

      <div
        style={{
          marginLeft: "240px",
          marginTop: "60px",
          padding: "25px",
          minHeight: "100vh",
          background: "#F4F2FF",
        }}
      >
        {children}
      </div>
    </div>
  );
}
