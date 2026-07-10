import { BrowserRouter, Route, Routes } from "react-router-dom";

import AppLayout from "../components/layout/AppLayout.jsx";
import Dashboard from "../features/dashboard/Dashboard.jsx";
import Gallery from "../features/gallery/Gallery.jsx";
import Settings from "../features/settings/Settings.jsx";
import Studio from "../features/studio/Studio.jsx";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/studio" element={<Studio />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
