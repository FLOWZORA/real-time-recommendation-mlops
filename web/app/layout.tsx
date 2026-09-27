import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "RecommendationOS | Real-Time E-Commerce Recommendation Platform",
  description:
    "Multi-tenant production-style recommendation platform powered by Two-Tower PyTorch embeddings, Milvus ANN vector search, Feast feature store, streaming Kafka pipelines, and MLflow governance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#f4f7fa] text-slate-800 min-h-screen flex flex-col font-sans">
        <Navbar />
        <main className="flex-1">{children}</main>
        <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-400 glass-panel">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between space-y-2 sm:space-y-0">
            <div>RecommendationOS &copy; 2026. Built with Two-Tower Retrieval & MLOps Architecture.</div>
            <div className="flex items-center space-x-4 font-mono text-[11px]">
              <span className="text-emerald-400 flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span>FastAPI Serving (8080)</span>
              </span>
              <span>ANN Milvus / In-Memory</span>
              <span>Feast Store</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
