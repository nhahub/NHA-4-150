/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        forge: {
          bg: "#0B1020",
          panel: "#111827",
          card: "rgba(255,255,255,0.06)",
          border: "rgba(255,255,255,0.12)",
          primary: "#38BDF8",
          secondary: "#8B5CF6",
          success: "#22C55E",
          warning: "#F59E0B",
          error: "#EF4444",
          text: "#F8FAFC",
          muted: "#94A3B8",
        },
      },
      boxShadow: {
        glow: "0 0 32px rgba(56, 189, 248, 0.18)",
      },
    },
  },
  plugins: [],
};
