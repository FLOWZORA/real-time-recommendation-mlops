"use client";

import React, { useState, useEffect } from "react";
import { Sparkles, Play, Activity, Timer, Cpu, Database, AlertCircle, RefreshCw } from "lucide-react";
import { getRecommendations, RecommendationResponse, TEST_PERSONAS } from "@/lib/api";

export default function DashboardRecommendationsPage() {
  const [userId, setUserId] = useState("0");
  const [data, setData] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTestWithId = async (id: string) => {
    setUserId(id);
    setLoading(true);
    setError(null);
    try {
      const res = await getRecommendations(id, true);
      setData(res);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Failed to generate recommendations. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem("current_user_id") || "0" : "0";
    setUserId(saved);
    handleTestWithId(saved);
  }, []);

  const handleTest = () => handleTestWithId(userId);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <span>Inference & Candidate Scoring Inspector</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Query the live serving engine for any user ID and examine the retrieved candidate set, latency, and model explainability.
          </p>
        </div>
      </div>

      {/* Query Bar */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Target User ID:</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="e.g. 0, 42, 89"
            className="bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-cyan-500 w-44 font-mono font-bold"
          />
          <button
            onClick={handleTest}
            disabled={loading}
            className="px-5 py-2 rounded-xl bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white font-bold text-xs flex items-center space-x-2 shadow-md shadow-cyan-500/20 transition-all disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-white text-white" />
            <span>{loading ? "Generating..." : "Run Inference"}</span>
          </button>
        </div>

        {/* Quick Test Persona Selector */}
        <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mr-1">
            Quick Personas:
          </span>
          {TEST_PERSONAS.map((p) => (
            <button
              key={p.id}
              onClick={() => handleTestWithId(p.id)}
              className={`px-3 py-1 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all border ${
                userId === p.id
                  ? "bg-cyan-50 border-cyan-300 text-cyan-700 font-bold shadow-sm"
                  : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
              }`}
            >
              <span>{p.avatar}</span>
              <span>{p.name} ({p.role.split("&")[0].trim()})</span>
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-2xl flex items-center justify-between text-xs font-bold">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button
            onClick={handleTest}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            Retry
          </button>
        </div>
      )}

      {data && (
        <div className="space-y-6">
          {/* Metadata Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div className="bg-white p-4 rounded-xl border border-slate-200/90 shadow-sm">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">Serving Strategy</span>
              <div className="text-sm font-bold text-cyan-700 font-mono mt-1">{data.strategy}</div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200/90 shadow-sm">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">P95 Latency</span>
              <div className="text-sm font-bold text-emerald-700 font-mono mt-1">{data.latency_ms} ms</div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200/90 shadow-sm">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">Model Version</span>
              <div className="text-sm font-bold text-purple-700 font-mono mt-1">{data.model_version}</div>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200/90 shadow-sm">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">Cold Start User</span>
              <div className="text-sm font-bold text-slate-800 font-mono mt-1">
                {data.cold_start ? "True (Fallback Active)" : "False (Warm Features)"}
              </div>
            </div>
          </div>

          {/* Candidates Table */}
          <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
            <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <span className="text-xs font-bold uppercase text-slate-700 tracking-wider">
                Ranked Recommendations ({data.detailed_recommendations.length} Items)
              </span>
              <span className="text-xs text-slate-500 font-medium">Pipeline: Milvus ANN &rarr; PyTorch Two-Tower</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-white border-b border-slate-100 text-slate-500 uppercase font-mono text-[10px]">
                  <tr>
                    <th className="py-3 px-5">Rank</th>
                    <th className="py-3 px-5">Item ID</th>
                    <th className="py-3 px-5">Title</th>
                    <th className="py-3 px-5">Price</th>
                    <th className="py-3 px-5">Score</th>
                    <th className="py-3 px-5">Source Stage</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {data.detailed_recommendations.map((rec) => (
                    <tr key={rec.rank} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-5 font-bold text-slate-900">#{rec.rank}</td>
                      <td className="py-3 px-5 font-mono font-bold text-cyan-600">#{rec.item_id}</td>
                      <td className="py-3 px-5 font-bold text-slate-900">{rec.title}</td>
                      <td className="py-3 px-5 font-semibold text-slate-900">${Number(rec.price).toFixed(2)}</td>
                      <td className="py-3 px-5">
                        <span className="font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                          {(rec.score * 100).toFixed(1)}% Neural Match
                        </span>
                      </td>
                      <td className="py-3 px-5 font-mono text-[11px] text-slate-600 font-medium">{rec.source}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
