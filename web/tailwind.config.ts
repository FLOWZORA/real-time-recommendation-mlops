import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        datta: {
          sidebar: "#3f4d67",
          dark: "#1d2630",
          body: "#f4f7fa",
          primary: "#1dc4e9",
          secondary: "#a389d4",
          accent1: "#04a9f5",
          accent2: "#1de9b6",
          cardDark: "#2b2c2f",
          borderDark: "#393b3f",
        },
        brand: {
          50: "#f0f7ff",
          100: "#e0effe",
          500: "#0284c7",
          600: "#0369a1",
          700: "#075985",
        },
        slate: {
          850: "#151e2e",
          900: "#0f172a",
          950: "#090d16",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "sans-serif"],
        mono: ["var(--font-jetbrains)", "monospace"],
      },
      boxShadow: {
        datta: "0 1px 20px 0 rgba(69, 90, 100, 0.08)",
        "datta-lg": "0 8px 30px rgba(69, 90, 100, 0.12)",
      },
    },
  },
  plugins: [],
};
export default config;
