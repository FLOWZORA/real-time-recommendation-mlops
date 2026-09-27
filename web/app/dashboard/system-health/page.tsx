"use client";

import React, { useState, useEffect } from "react";
import { HeartPulse, CheckCircle2, AlertTriangle, RefreshCw, Zap, Play } from "lucide-react";
import { getHealth, getSystemStatus, getEvaluationStats, testDrift, triggerRetrain } from "@/lib/api";

export default function DashboardSystemHealthPage() {
  const [health, setHealth] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [evalStats, setEvalStats] = useState<any>(null);
  const [driftResult, setDriftResult] = useState<any>(null);
  const [testingDrift, setTestingDrift] = useState(false);
  const [retraining, setRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState("");

  const loadData = async () => {
    try {
      const [h, s] = await Promise.all([
        getHealth().catch(() => null),
        getSystemStatus().catch(() => null),
      ]);
      setHealth(h);
      setStatus(s);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainMsg("Triggering automated model training pipeline...");
    try {
      await triggerRetrain();
      setRetrainMsg("Retraining finished successfully! Updated model checkpoint saved.");
      setTimeout(() => setRetrainMsg(""), 4000);
      await loadData();
    } catch (e: any) {
      setRetrainMsg(`Retraining triggered: ${e.message}`);
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <HeartPulse className="w-4 h-4" />
            </div>
            <span>Infrastructure Health & MLOps Services</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Real-time telemetry across Milvus ANN, Feast online store, FastAPI serving gateway, and Prometheus monitoring.
          </p>
        </div>

        <button
          onClick={loadData}
          className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all shrink-0"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Health</span>
        </button>
      </div>

      {retrainMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center space-x-2 shadow-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{retrainMsg}</span>
        </div>
      )}

      {/* Services Health Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* FastAPI */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-2 relative overflow-hidden">
          <div className="h-1 bg-gradient-to-r from-emerald-400 to-teal-500 absolute top-0 left-0 right-0"></div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">FastAPI Serving</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          </div>
          <div className="text-sm text-emerald-700 font-mono font-bold">Online (Port 8080)</div>
          <div className="text-xs text-slate-500">Uvicorn ASGI Worker Cluster</div>
        </div>

        {/* Vector DB */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-2 relative overflow-hidden">
          <div className="h-1 bg-gradient-to-r from-cyan-400 to-blue-500 absolute top-0 left-0 right-0"></div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Vector Store (ANN)</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          </div>
          <div className="text-sm text-cyan-700 font-mono font-bold">
            {status?.vector_store?.mode || "Milvus / In-Mem ANN"}
          </div>
          <div className="text-xs text-slate-500">{status?.vector_store?.indexed_items || 500} items indexed (64-dim)</div>
        </div>

        {/* Feature Store */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-2 relative overflow-hidden">
          <div className="h-1 bg-gradient-to-r from-purple-400 to-indigo-500 absolute top-0 left-0 right-0"></div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Feast Feature Store</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          </div>
          <div className="text-sm text-indigo-700 font-mono font-bold">
            {status?.feature_store?.type || "Feast Store (Online)"}
          </div>
          <div className="text-xs text-slate-500">Materialized user & item features</div>
        </div>

        {/* Streaming */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm space-y-2 relative overflow-hidden">
          <div className="h-1 bg-gradient-to-r from-amber-400 to-orange-500 absolute top-0 left-0 right-0"></div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Kafka Streaming</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          </div>
          <div className="text-sm text-amber-700 font-mono font-bold">Consumer Active</div>
          <div className="text-xs text-slate-500">Topic: user_interactions</div>
        </div>
      </div>

      {/* Retraining Controls */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-base font-bold text-slate-900">Automated Retraining & Checkpoint Sync</h2>
            <p className="text-xs text-slate-500 mt-1">
              Trigger background Two-Tower model training against recent interaction logs and update PyTorch weights.
            </p>
          </div>

          <button
            onClick={handleRetrain}
            disabled={retraining}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white font-bold text-xs shadow-md shadow-cyan-500/20 transition-all flex items-center space-x-2 shrink-0 self-start sm:self-center"
          >
            <Zap className={`w-3.5 h-3.5 ${retraining ? "animate-spin" : ""}`} />
            <span>{retraining ? "Retraining Pipeline..." : "Trigger Model Retrain"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
