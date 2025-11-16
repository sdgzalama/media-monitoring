import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import MediaItems from "./pages/MediaItems";
import ProjectAnalytics from "./pages/ProjectAnalytics";  
import CreateClient from "./pages/CreateClient";
import CreateProject from "./pages/CreateProject";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/media-items" element={<MediaItems />} />
        <Route path="/analytics/:id" element={<ProjectAnalytics />} />
        <Route path="/clients/new" element={<CreateClient />} />
        <Route path="/projects/new" element={<CreateProject />} />


      </Routes>
    </BrowserRouter>
  );
}


