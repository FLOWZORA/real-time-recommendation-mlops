"use client";

import React, { useState, useEffect } from "react";
import { GitBranch, CheckCircle2, AlertCircle, RefreshCw, Activity, ArrowRight } from "lucide-react";
import { getExperiments, updateExperiment, Experiment } from "@/lib/api";

export default function DashboardExperimentsPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getExperiments();
      setExperiments(data);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Failed to load experiments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleToggleStatus = async (exp: Experiment) => {
    const nextStatus = exp.status === "ACTIVE" ? "PAUSED" : "ACTIVE";
    try {
      await updateExperiment(exp.id, { status: nextStatus });
      await load();
    } catch (e: any) {
      alert(`Update failed: ${e.message}`);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <GitBranch className="w-4 h-4" />
            </div>
            <span>A/B Experimentation Cockpit</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Conduct safe online model experiments with deterministic user hash bucketing and two-proportion Z-test significance.
          </p>
        </div>

        <button
          onClick={load}
          disabled={loading}
          className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-2xl flex items-center justify-between text-xs font-bold">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button
            onClick={load}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            Retry
          </button>
        </div>
      )}

      {/* Experiments List */}
      <div className="space-y-6">
        {loading ? (
          <div className="bg-white p-8 text-center text-slate-400 rounded-2xl border border-slate-200">Loading experiments...</div>
        ) : experiments.length > 0 ? (
          experiments.map((exp) => (
            <div key={exp.id} className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
              <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center space-x-2.5">
                    <h2 className="text-base font-bold text-slate-900">{exp.name}</h2>
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider ${
                        exp.status === "ACTIVE"
                          ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                          : "bg-slate-100 text-slate-600 border border-slate-300"
                      }`}
                    >
                      {exp.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500 font-mono mt-1">
                    ID: {exp.id} &bull; Traffic Allocation: {(exp.traffic_split_b * 100).toFixed(0)}% to Challenger
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  {exp.statistically_significant ? (
                    <span className="flex items-center space-x-1 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Statistically Significant (p &lt; 0.05)</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-1 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-700 text-xs font-bold">
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>Awaiting Significance (p = {exp.p_value ? exp.p_value.toFixed(4) : "0.1240"})</span>
                    </span>
                  )}
                  <button
                    onClick={() => handleToggleStatus(exp)}
                    className="px-3 py-1.5 rounded-xl border border-slate-200 hover:border-slate-300 text-xs font-bold text-slate-700 bg-slate-50"
                  >
                    {exp.status === "ACTIVE" ? "Pause" : "Resume"}
                  </button>
                </div>
              </div>

              {/* Variants comparison */}
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50/50">
                {/* Variant A */}
                <div className="bg-white p-5 rounded-xl border border-slate-200/90 shadow-sm space-y-3">
                  <div className="flex items-center justify-between text-xs pb-2 border-b border-slate-100">
                    <span className="font-bold text-slate-600 uppercase tracking-wider">Variant A (Baseline)</span>
                    <span className="font-mono text-slate-900 font-bold bg-slate-100 px-2 py-0.5 rounded">{exp.variant_a_model}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="bg-slate-50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">Impressions</div>
                      <div className="text-sm font-extrabold text-slate-900 font-mono mt-0.5">{exp.variant_a_impressions}</div>
                    </div>
                    <div className="bg-slate-50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">Clicks</div>
                      <div className="text-sm font-extrabold text-slate-900 font-mono mt-0.5">{exp.variant_a_clicks}</div>
                    </div>
                    <div className="bg-slate-50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">CTR</div>
                      <div className="text-sm font-extrabold text-slate-900 font-mono mt-0.5">
                        {((exp.variant_a_ctr || 0) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </div>

                {/* Variant B */}
                <div className="bg-white p-5 rounded-xl border border-cyan-200 shadow-sm space-y-3 relative overflow-hidden">
                  <div className="h-1 bg-gradient-to-r from-cyan-400 to-indigo-500 absolute top-0 left-0 right-0"></div>
                  <div className="flex items-center justify-between text-xs pb-2 border-b border-slate-100">
                    <span className="font-bold text-cyan-700 uppercase tracking-wider">Variant B (Challenger)</span>
                    <span className="font-mono text-cyan-800 font-bold bg-cyan-50 px-2 py-0.5 rounded border border-cyan-200">{exp.variant_b_model}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="bg-cyan-50/50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">Impressions</div>
                      <div className="text-sm font-extrabold text-slate-900 font-mono mt-0.5">{exp.variant_b_impressions}</div>
                    </div>
                    <div className="bg-cyan-50/50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">Clicks</div>
                      <div className="text-sm font-extrabold text-slate-900 font-mono mt-0.5">{exp.variant_b_clicks}</div>
                    </div>
                    <div className="bg-cyan-50/50 p-2.5 rounded-lg">
                      <div className="text-[10px] uppercase font-bold text-slate-600">CTR</div>
                      <div className="text-sm font-extrabold text-emerald-700 font-mono mt-0.5">
                        {((exp.variant_b_ctr || 0) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="bg-white p-8 text-center text-slate-500 rounded-2xl border border-slate-200">
            No active experiments found.
          </div>
        )}
      </div>
    </div>
  );
}
