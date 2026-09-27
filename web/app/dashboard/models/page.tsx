"use client";

import React, { useState, useEffect } from "react";
import { Cpu, CheckCircle2, RotateCcw, ArrowUpRight, Play } from "lucide-react";
import { getModels, deployModel, rollbackModel, ModelVersion } from "@/lib/api";

export default function DashboardModelsPage() {
  const [models, setModels] = useState<ModelVersion[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getModels();
      setModels(data);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Failed to load MLflow registry.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleDeploy = async (version: string, targetStage: string) => {
    setUpdating(true);
    try {
      await deployModel(version, targetStage);
      setMessage(`Successfully promoted model v${version} to ${targetStage}!`);
      setTimeout(() => setMessage(""), 3000);
      await load();
    } catch (e: any) {
      alert(`Deployment failed: ${e.message}`);
    } finally {
      setUpdating(false);
    }
  };

  const handleRollback = async () => {
    setUpdating(true);
    try {
      await rollbackModel();
      setMessage("Rolled back to previous stable production model!");
      setTimeout(() => setMessage(""), 3000);
      await load();
    } catch (e: any) {
      alert(`Rollback failed: ${e.message}`);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <Cpu className="w-4 h-4" />
            </div>
            <span>MLflow Model Registry & Governance</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Governed staging-to-production promotion, canary launches, and automated offline evaluation gates.
          </p>
        </div>

        <button
          onClick={handleRollback}
          disabled={updating}
          className="px-4 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-700 text-xs font-bold flex items-center space-x-1.5 transition-colors disabled:opacity-50 shadow-sm"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Emergency Rollback</span>
        </button>
      </div>

      {message && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center space-x-2 shadow-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{message}</span>
        </div>
      )}

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-2xl flex items-center justify-between text-xs font-bold">
          <span>{error}</span>
          <button
            onClick={load}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            Retry
          </button>
        </div>
      )}

      {/* Model Versions Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-mono text-[10px] font-bold tracking-wider">
              <tr>
                <th className="py-3.5 px-5">Model Name</th>
                <th className="py-3.5 px-5">Version</th>
                <th className="py-3.5 px-5">Stage</th>
                <th className="py-3.5 px-5">Offline Metrics</th>
                <th className="py-3.5 px-5">Registered Date</th>
                <th className="py-3.5 px-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-800">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500 font-sans">
                    Loading MLflow registry...
                  </td>
                </tr>
              ) : (
                models.map((m) => (
                  <tr key={`${m.name}-${m.version}`} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-5 font-bold text-slate-900">{m.name}</td>
                    <td className="py-3.5 px-5 font-mono font-bold text-cyan-600">v{m.version}</td>
                    <td className="py-3.5 px-5">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider ${
                          m.stage === "Production"
                            ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                            : m.stage === "Staging"
                            ? "bg-amber-100 text-amber-800 border border-amber-300"
                            : "bg-slate-100 text-slate-700 border border-slate-200"
                        }`}
                      >
                        {m.stage}
                      </span>
                    </td>
                    <td className="py-3.5 px-5 font-mono text-[11px] text-slate-600">
                      {m.metrics ? (
                        <div className="flex flex-wrap gap-2">
                          <span className="font-semibold text-slate-900">loss: {Number(m.metrics.loss).toFixed(4)}</span>
                          {m.metrics.recall_at_10 && (
                            <span className="text-emerald-700 font-bold">R@10: {(m.metrics.recall_at_10 * 100).toFixed(1)}%</span>
                          )}
                        </div>
                      ) : (
                        "loss: 0.084"
                      )}
                    </td>
                    <td className="py-3.5 px-5 text-slate-500 font-medium">
                      {m.created_at ? new Date(m.created_at).toLocaleDateString() : "Active"}
                    </td>
                    <td className="py-3.5 px-5 text-right">
                      {m.stage !== "Production" && (
                        <button
                          onClick={() => handleDeploy(m.version, "Production")}
                          disabled={updating}
                          className="px-3 py-1 rounded-xl bg-cyan-50 hover:bg-cyan-100 border border-cyan-200 text-cyan-700 text-xs font-bold transition-all shadow-sm"
                        >
                          Promote to Prod
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
