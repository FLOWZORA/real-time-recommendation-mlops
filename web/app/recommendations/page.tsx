"use client";

import React, { useState, useEffect } from "react";
import {
  Sparkles,
  Activity,
  Layers,
  Zap,
  RefreshCw,
  Cpu,
  BarChart,
  Eye,
  MousePointer,
  ShoppingBag,
} from "lucide-react";
import ProductCard from "@/components/ProductCard";
import {
  getRecommendations,
  sendEvent,
  RecommendationResponse,
  TEST_PERSONAS,
} from "@/lib/api";

export default function RecommendationsLabPage() {
  const [selectedUserId, setSelectedUserId] = useState("0");
  const [recs, setRecs] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState(false);

  const persona = TEST_PERSONAS.find((p) => p.id === selectedUserId) || TEST_PERSONAS[0];

  const fetchRecs = async (uid: string) => {
    setLoading(true);
    try {
      const data = await getRecommendations(uid, true);
      setRecs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecs(selectedUserId);
  }, [selectedUserId]);

  const handleAction = async (actionType: string, itemId: number) => {
    setActing(true);
    try {
      await sendEvent(selectedUserId, itemId, actionType);
      setTimeout(() => {
        fetchRecs(selectedUserId);
        setActing(false);
      }, 600);
    } catch (e) {
      setActing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div className="datta-card p-6 bg-white dark:bg-[#2b2c2f] border border-slate-200/80 dark:border-slate-800">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-50 dark:bg-cyan-950/60 border border-cyan-200 dark:border-cyan-800 text-cyan-600 dark:text-cyan-400 text-xs font-bold mb-2">
          <Activity className="w-3.5 h-3.5" />
          <span>Real-Time Model Inference & Online Learning Console</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          Personalized Recommendation Lab
        </h1>
        <p className="text-xs text-slate-600 mt-1">
          Inspect Two-Tower PyTorch embeddings, Feast online features, and real-time online learning policy adaptations.
        </p>
      </div>

      {/* Persona Selection Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {TEST_PERSONAS.map((p) => (
          <button
            key={p.id}
            onClick={() => setSelectedUserId(p.id)}
            className={`p-4 rounded-2xl border text-left transition-all shadow-sm ${
              selectedUserId === p.id
                ? "bg-cyan-50 border-cyan-500 ring-2 ring-cyan-500/20"
                : "bg-white border-slate-200 hover:border-cyan-400"
            }`}
          >
            <div className="text-2xl mb-2">{p.avatar}</div>
            <div className="font-bold text-xs text-slate-900">{p.name}</div>
            <div className="text-[11px] text-slate-500 font-medium truncate">{p.segment}</div>
          </button>
        ))}
      </div>

      {/* Model State & Telemetry Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Feast Features */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase text-slate-700 flex items-center space-x-1.5">
              <Layers className="w-4 h-4 text-cyan-600" />
              <span>Feast Online Store</span>
            </span>
            <span className="text-[10px] font-mono text-cyan-700 bg-cyan-50 border border-cyan-200 px-2 py-0.5 rounded-md font-bold">
              user_id: {selectedUserId}
            </span>
          </div>

          <div className="space-y-2 pt-1 font-mono text-xs">
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">total_views</span>
              <span className="font-bold text-cyan-700">{recs?.user_features?.total_views ?? 0}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">total_clicks</span>
              <span className="font-bold text-emerald-700">{recs?.user_features?.total_clicks ?? 0}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">total_purchases</span>
              <span className="font-bold text-purple-700">{recs?.user_features?.total_purchases ?? 0}</span>
            </div>
          </div>
        </div>

        {/* Serving Strategy & Pipeline */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase text-slate-700 flex items-center space-x-1.5">
              <Cpu className="w-4 h-4 text-purple-600" />
              <span>Pipeline Routing</span>
            </span>
            <span className="text-[10px] font-mono text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md font-bold">
              ONLINE
            </span>
          </div>

          <div className="space-y-2 pt-1 font-mono text-xs">
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">strategy</span>
              <span className="font-bold text-purple-700">{recs?.strategy ?? "neural_two_tower"}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">latency</span>
              <span className="font-bold text-emerald-700">{recs?.latency_ms ? `${recs.latency_ms} ms` : "12.4 ms"}</span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
              <span className="text-slate-600 font-semibold">model_version</span>
              <span className="font-bold text-cyan-700">{recs?.model_version ?? "two_tower_v2"}</span>
            </div>
          </div>
        </div>

        {/* Model Explanation */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase text-slate-700 flex items-center space-x-1.5">
                <Sparkles className="w-4 h-4 text-amber-500" />
                <span>Explainable AI</span>
              </span>
              <span className="text-[10px] font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md">
                Confidence: High
              </span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {recs?.explanation || "Candidate retrieval matched via cosine similarity against Milvus ANN index, re-ranked with diversity penalties."}
            </p>
          </div>

          <button
            onClick={() => fetchRecs(selectedUserId)}
            disabled={loading}
            className="w-full mt-4 py-2 px-3 text-xs font-bold rounded-xl bg-slate-900 hover:bg-slate-800 text-white transition-all flex items-center justify-center space-x-1.5 shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Re-query Serving Pipeline</span>
          </button>
        </div>
      </div>

      {/* Recommended Items Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-black text-slate-900">
            Candidates Scored for {persona.name}
          </h2>
          <span className="text-xs text-slate-600 font-mono font-bold">
            {recs?.detailed_recommendations?.length || 0} Ranked Items
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {recs?.detailed_recommendations?.map((item) => (
            <ProductCard key={item.item_id} product={item} showScore={true} />
          ))}
        </div>
      </div>
    </div>
  );
}
