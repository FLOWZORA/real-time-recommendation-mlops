"use client";

import React, { useState, useEffect } from "react";
import { Activity, RefreshCw, Eye, MousePointer, ShoppingBag, Radio } from "lucide-react";
import { getEvents } from "@/lib/api";

export default function DashboardEventsPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
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
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
            <span>Kafka Streaming Event Log</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Real-time Kafka ingestion log tracking views, clicks, and conversion rewards into Feast online features.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Streaming Active (5s Poll)
          </span>
          <button
            onClick={load}
            disabled={loading}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Events Table Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase text-[10px] tracking-wider">
              <tr>
                <th className="py-3.5 px-5">Event ID</th>
                <th className="py-3.5 px-5">User ID</th>
                <th className="py-3.5 px-5">Item Numeric ID</th>
                <th className="py-3.5 px-5">Event Type</th>
                <th className="py-3.5 px-5">Reward Weight</th>
                <th className="py-3.5 px-5">Timestamp</th>
                <th className="py-3.5 px-5">Feast Sync</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                [...Array(6)].map((_, i) => (
                  <tr key={i} className="animate-pulse">
                    <td colSpan={7} className="py-4 px-5 text-center text-slate-400">Polling Kafka interaction stream...</td>
                  </tr>
                ))
              ) : events.length > 0 ? (
                events.map((ev, idx) => (
                  <tr key={ev.id || idx} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-5 font-mono text-slate-500">{ev.id || `ev_${idx + 1}`}</td>
                    <td className="py-3.5 px-5 font-bold text-slate-900">{ev.user_id}</td>
                    <td className="py-3.5 px-5 font-mono font-bold text-cyan-600">Product #{ev.item_id_numeric}</td>
                    <td className="py-3.5 px-5">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider ${
                          ev.event_type === "purchase"
                            ? "bg-purple-100 text-purple-800 border border-purple-200"
                            : ev.event_type === "add_to_cart"
                            ? "bg-amber-100 text-amber-800 border border-amber-200"
                            : ev.event_type === "click"
                            ? "bg-cyan-100 text-cyan-800 border border-cyan-200"
                            : "bg-slate-100 text-slate-700 border border-slate-200"
                        }`}
                      >
                        {ev.event_type}
                      </span>
                    </td>
                    <td className="py-3.5 px-5 font-mono font-bold text-slate-900">
                      {ev.event_type === "purchase" ? "+5.0" : ev.event_type === "add_to_cart" ? "+3.0" : ev.event_type === "click" ? "+1.0" : "+0.1"}
                    </td>
                    <td className="py-3.5 px-5 text-slate-500 font-medium">
                      {new Date(ev.created_at).toLocaleTimeString()}
                    </td>
                    <td className="py-3.5 px-5">
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700">
                        <Radio className="w-3 h-3 text-emerald-600 animate-pulse" />
                        Materialized
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-slate-500">
                    No events captured yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
