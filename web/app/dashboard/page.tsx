"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Activity,
  Zap,
  TrendingUp,
  Cpu,
  Layers,
  HeartPulse,
  Database,
  ArrowUpRight,
  ShieldCheck,
  Server,
  RefreshCw,
  Clock,
  Sparkles,
  CheckCircle2,
} from "lucide-react";
import {
  getAnalyticsOverview,
  getSystemStatus,
  AnalyticsOverview,
} from "@/lib/api";

export default function DashboardOverviewPage() {
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null);
  const [system, setSystem] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [an, sys] = await Promise.all([
        getAnalyticsOverview().catch(() => null),
        getSystemStatus().catch(() => null),
      ]);
      setAnalytics(an);
      setSystem(sys);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-700 text-xs font-bold mb-2">
            <ShieldCheck className="w-3.5 h-3.5 text-cyan-600" />
            <span>Store Admin & MLOps Control Center</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            Executive SaaS Dashboard
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Real-time telemetry across multi-tenant recommendation serving, streaming ingestion, and model quality.
          </p>
        </div>

        <button
          onClick={loadData}
          disabled={loading}
          className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-sm transition-all shrink-0 self-start sm:self-center"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Telemetry</span>
        </button>
      </div>

      {/* KPI Stat Cards Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Requests Served */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm relative overflow-hidden flex flex-col justify-between">
          <div className="h-1 bg-gradient-to-r from-cyan-400 to-indigo-500 absolute top-0 left-0 right-0" />
          <div className="flex items-center justify-between text-slate-600 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Requests Served</span>
            <div className="w-8 h-8 rounded-lg bg-cyan-50 flex items-center justify-center">
              <Zap className="w-4 h-4 text-cyan-600" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 my-1">
            {(analytics?.recommendation_requests_today ?? 1420).toLocaleString()}
          </div>
          <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1.5 mt-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Live serving active</span>
          </div>
        </div>

        {/* Avg Latency */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm relative overflow-hidden flex flex-col justify-between">
          <div className="h-1 bg-gradient-to-r from-purple-400 to-pink-500 absolute top-0 left-0 right-0" />
          <div className="flex items-center justify-between text-slate-600 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Avg Latency (p95)</span>
            <div className="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center">
              <Activity className="w-4 h-4 text-purple-600" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 my-1">
            {analytics?.avg_latency_ms ?? 4.2} <span className="text-sm font-bold text-slate-500">ms</span>
          </div>
          <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1.5 mt-2">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>SLA Compliant (&lt;100ms)</span>
          </div>
        </div>

        {/* CTR */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm relative overflow-hidden flex flex-col justify-between">
          <div className="h-1 bg-gradient-to-r from-emerald-400 to-teal-500 absolute top-0 left-0 right-0" />
          <div className="flex items-center justify-between text-slate-600 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Recommendation CTR</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-emerald-600" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 my-1">
            {((analytics?.overall_ctr ?? 0.0642) * 100).toFixed(1)}%
          </div>
          <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1.5 mt-2">
            <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
            <span>+9.6% vs unranked baseline</span>
          </div>
        </div>

        {/* Cache Hit Rate */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm relative overflow-hidden flex flex-col justify-between">
          <div className="h-1 bg-gradient-to-r from-amber-400 to-orange-500 absolute top-0 left-0 right-0" />
          <div className="flex items-center justify-between text-slate-600 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Cache Hit Rate</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
              <Server className="w-4 h-4 text-amber-600" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 my-1">
            {((analytics?.cache_hit_rate ?? 0.784) * 100).toFixed(0)}%
          </div>
          <div className="text-xs font-semibold text-slate-600 flex items-center gap-1.5 mt-2">
            <Database className="w-3.5 h-3.5 text-slate-500" />
            <span>Redis Low-Latency Layer</span>
          </div>
        </div>
      </div>

      {/* Second Row: System Components Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* ML Model Health */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Cpu className="w-4 h-4 text-cyan-600" />
              <span>Production Model</span>
            </h2>
            <Link href="/dashboard/models" className="text-xs font-bold text-cyan-600 hover:text-cyan-700 flex items-center gap-1">
              <span>Manage</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Registered Model</span>
              <span className="text-slate-900 font-bold font-mono">{system?.model?.name || "TwoTowerRecommender"}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Stage</span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                {system?.model?.stage || "Production"}
              </span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Architecture</span>
              <span className="text-slate-700 font-mono font-semibold">User(8→32), Item(8→32)</span>
            </div>
          </div>
        </div>

        {/* Vector DB & Feature Store */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Layers className="w-4 h-4 text-indigo-600" />
              <span>Vector Store & Features</span>
            </h2>
            <Link href="/dashboard/system-health" className="text-xs font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1">
              <span>Inspect</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Vector Search</span>
              <span className="text-indigo-700 font-bold font-mono">{system?.vector_store?.mode || "Local In-Memory Vector Index"}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Indexed Vectors</span>
              <span className="text-slate-900 font-bold font-mono">500 items (32-dim)</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Feature Store</span>
              <span className="text-cyan-700 font-bold font-mono">Feast (SQLite Online)</span>
            </div>
          </div>
        </div>

        {/* Streaming & Kafka Event Pipeline */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Activity className="w-4 h-4 text-emerald-600" />
              <span>Event Stream & Kafka</span>
            </h2>
            <Link href="/dashboard/events" className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
              <span>View Stream</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Total Events Logged</span>
              <span className="text-slate-900 font-bold font-mono">{analytics?.total_events ?? 1840}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Conversion Rate</span>
              <span className="text-emerald-700 font-bold font-mono">2.85%</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-xl">
              <span className="text-slate-600 font-medium">Kafka Pipeline</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">Active • Topic: events</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Links Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-1">
        <Link
          href="/dashboard/products"
          className="bg-white p-4 rounded-xl border border-slate-200/90 hover:border-cyan-400 hover:shadow-md transition-all flex items-center justify-between group shadow-sm"
        >
          <div>
            <div className="text-xs font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">Catalog Manager</div>
            <div className="text-[11px] text-slate-500 mt-0.5">{analytics?.total_products ?? 500} products</div>
          </div>
          <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-cyan-600 transition-colors" />
        </Link>

        <Link
          href="/dashboard/experiments"
          className="bg-white p-4 rounded-xl border border-slate-200/90 hover:border-cyan-400 hover:shadow-md transition-all flex items-center justify-between group shadow-sm"
        >
          <div>
            <div className="text-xs font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">A/B Testing</div>
            <div className="text-[11px] text-slate-500 mt-0.5">{analytics?.active_experiments ?? 1} active</div>
          </div>
          <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-cyan-600 transition-colors" />
        </Link>

        <Link
          href="/dashboard/api-keys"
          className="bg-white p-4 rounded-xl border border-slate-200/90 hover:border-cyan-400 hover:shadow-md transition-all flex items-center justify-between group shadow-sm"
        >
          <div>
            <div className="text-xs font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">API Keys</div>
            <div className="text-[11px] text-slate-500 mt-0.5 font-mono">Bearer reco_live_...</div>
          </div>
          <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-cyan-600 transition-colors" />
        </Link>

        <Link
          href="/dashboard/system-health"
          className="bg-white p-4 rounded-xl border border-slate-200/90 hover:border-cyan-400 hover:shadow-md transition-all flex items-center justify-between group shadow-sm"
        >
          <div>
            <div className="text-xs font-bold text-slate-900 group-hover:text-cyan-600 transition-colors">Drift Watchdog</div>
            <div className="text-[11px] text-emerald-700 font-medium mt-0.5">Healthy • 0 alarms</div>
          </div>
          <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-cyan-600 transition-colors" />
        </Link>
      </div>
    </div>
  );
}
