import { Menu, RadioTower } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";

import Logo2 from "../../assets/Logo2.png";

const titles = {
  "/": ["VisualForge AI", "AI Visual Content Studio"],
  "/studio": ["Studio", "Generate, edit, and refine visual outputs"],
  "/gallery": ["Gallery", "Generation history and output archive"],
  "/settings": ["Settings", "API status and system readiness"],
};

const mobileLinks = [
  { to: "/", label: "Dashboard" },
  { to: "/studio", label: "Studio" },
  { to: "/gallery", label: "Gallery" },
  { to: "/settings", label: "Settings" },
];

export default function Header() {
  const location = useLocation();
  const [title, subtitle] = titles[location.pathname] || titles["/"];

  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-forge-bg/[0.82] backdrop-blur-xl">
      <div className="flex min-h-20 items-center justify-between gap-4 px-4 md:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <img src={Logo2} alt="" className="h-9 w-9 object-contain md:hidden" />
          <div className="min-w-0">
            <h1 className="truncate text-xl font-semibold text-forge-text md:text-2xl">
              {title}
            </h1>
            <p className="truncate text-sm text-forge-muted">{subtitle}</p>
          </div>
        </div>
        <div className="hidden items-center gap-2 rounded-md border border-emerald-400/20 bg-emerald-400/10 px-3 py-2 text-sm text-emerald-100 sm:flex">
          <RadioTower size={16} />
          <span>Local API</span>
        </div>
        <div className="md:hidden">
          <Menu size={22} className="text-forge-muted" />
        </div>
      </div>
      <nav className="flex gap-2 overflow-x-auto border-t border-white/[0.08] px-4 py-2 md:hidden">
        {mobileLinks.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `rounded-md px-3 py-2 text-sm font-semibold transition ${
                isActive
                  ? "bg-forge-primary/[0.18] text-forge-text"
                  : "text-forge-muted hover:bg-white/[0.08] hover:text-forge-text"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
