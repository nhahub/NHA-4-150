import {
  BarChart3,
  ChevronLeft,
  ChevronRight,
  Image,
  Settings,
  Sparkles,
} from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

import Logo from "../../assets/Logo.png";
import Logo2 from "../../assets/Logo2.png";
import Button from "../ui/Button.jsx";

const navItems = [
  { to: "/", label: "Dashboard", icon: BarChart3 },
  { to: "/studio", label: "Studio", icon: Sparkles },
  { to: "/gallery", label: "Gallery", icon: Image },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`hidden min-h-screen shrink-0 border-r border-white/10 bg-forge-panel/70 backdrop-blur-xl transition-all md:flex md:flex-col ${collapsed ? "w-[84px]" : "w-[276px]"}`}
    >
      <div className="flex h-20 items-center justify-between px-4">
        <NavLink to="/" className="flex min-w-0 items-center gap-3">
          {collapsed ? (
            <img src={Logo2} alt="VisualForge AI" className="h-10 w-10 object-contain" />
          ) : (
            <img src={Logo} alt="VisualForge AI" className="h-12 max-w-[188px] object-contain" />
          )}
        </NavLink>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed((value) => !value)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          title={collapsed ? "Expand" : "Collapse"}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </Button>
      </div>

      <nav className="flex flex-1 flex-col gap-2 px-3 py-4">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            title={collapsed ? label : undefined}
            className={({ isActive }) =>
              `focus-ring flex h-12 items-center gap-3 rounded-md px-3 text-sm font-semibold transition ${
                isActive
                  ? "bg-forge-primary/[0.16] text-forge-text shadow-glow"
                  : "text-forge-muted hover:bg-white/[0.08] hover:text-forge-text"
              } ${collapsed ? "justify-center" : ""}`
            }
          >
            <Icon size={19} />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
