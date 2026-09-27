"use client";

import React, { useState, useEffect } from "react";
import { Activity, RefreshCw, Eye, MousePointer, ShoppingBag, Zap } from "lucide-react";
import { getEvents } from "@/lib/api";

export default function HistoryEventsPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const data = await getEvents(50);
      setEvents(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const getActionBadge = (action: string) => {
    switch (action) {
      case "purchase":
        return {
          icon: ShoppingBag,
          color: "bg-purple-100 text-purple-700 border-purple-200",
          reward: "+1.0 (High)",
        };
      case "product_click":
      case "click":
      case "add_to_cart":
        return {
          icon: MousePointer,
          color: "bg-cyan-100 text-cyan-700 border-cyan-200",
          reward: "+0.5 (Medium)",
        };
      default:
        return {
          icon: Eye,
          color: "bg-slate-100 text-slate-700 border-slate-200",
          reward: "+0.1 (Low)",
        };
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
            <span>Behavioral Event Stream</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Real-time feed of all user interactions ingested via FastAPI, streamed to Kafka, and logged for offline counterfactual evaluation.
          </p>
        </div>

        <button
          onClick={loadEvents}
          disabled={loading}
          className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-sm transition-all shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs">Loading event stream...</div>
        ) : events.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs">
            No events logged yet. Interact with products or simulate clicks to populate this feed.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {events.map((ev) => {
              const badge = getActionBadge(ev.event_type);
              const Icon = badge.icon;
              return (
                <div key={ev.id} className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div className={`p-2.5 rounded-xl border ${badge.color}`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-slate-900 capitalize">
                          {ev.event_type.replace("_", " ")}
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md bg-cyan-50 text-cyan-700 border border-cyan-200">
                          Item #{ev.item_id_numeric}
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                          Materialized
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-500 font-mono mt-0.5">
                        User ID: <span className="font-bold text-slate-800">{ev.user_id}</span> &bull; Reward: <span className="font-bold text-emerald-700">{badge.reward}</span>
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-[11px] font-mono font-semibold text-slate-700">
                      {new Date(ev.created_at).toLocaleTimeString()}
                    </div>
                    <div className="text-[10px] text-slate-400">
                      {new Date(ev.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
