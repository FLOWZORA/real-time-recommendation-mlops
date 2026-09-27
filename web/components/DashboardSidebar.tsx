"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Package,
  Activity,
  Sparkles,
  Cpu,
  GitBranch,
  BarChart3,
  HeartPulse,
  KeyRound,
  ArrowLeft,
  Store,
} from "lucide-react";

const NAV_GROUPS = [
  {
    title: "Navigation",
    items: [
      { href: "/dashboard", label: "Live Overview", icon: LayoutDashboard },
    ],
  },
  {
    title: "Platform & Catalog",
    items: [
      { href: "/dashboard/products", label: "Catalog Manager", icon: Package },
      { href: "/dashboard/events", label: "Live Event Stream", icon: Activity },
      { href: "/dashboard/recommendations", label: "Inference Inspector", icon: Sparkles },
    ],
  },
  {
    title: "MLOps & Governance",
    items: [
      { href: "/dashboard/models", label: "MLflow Models", icon: Cpu },
      { href: "/dashboard/experiments", label: "A/B Testing", icon: GitBranch },
      { href: "/dashboard/analytics", label: "Analytics & KPIs", icon: BarChart3 },
    ],
  },
  {
    title: "System & Security",
    items: [
      { href: "/dashboard/system-health", label: "System Health", icon: HeartPulse },
      { href: "/dashboard/api-keys", label: "API Keys", icon: KeyRound },
    ],
  },
];

export default function DashboardSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#3f4d67] text-[#a9b7d0] flex flex-col justify-between h-[calc(100vh-4rem)] sticky top-16 shrink-0 shadow-lg">
      <div className="p-4 space-y-6 overflow-y-auto">
        {/* Brand Bar in Sidebar */}
        <div className="px-2 pt-1 pb-2 border-b border-slate-600/40">
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#e8edf7] font-bold">
            RecommendationOS Admin
          </div>
          <div className="text-[11px] text-cyan-300 font-mono mt-0.5">
            MLOps & Serving Engine
          </div>
        </div>

        {/* Navigation Groups */}
        <div className="space-y-5">
          {NAV_GROUPS.map((group) => (
            <div key={group.title}>
              <div className="text-[10px] font-bold uppercase tracking-wider text-[#e8edf7]/60 px-3 mb-1.5">
                {group.title}
              </div>
              <nav className="space-y-0.5">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center space-x-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                        isActive
                          ? "bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] text-white shadow-md shadow-cyan-500/20"
                          : "text-[#a9b7d0] hover:text-white hover:bg-slate-700/40"
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-[#a9b7d0]"}`} />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>
      </div>

      {/* Footer link to Storefront */}
      <div className="p-4 border-t border-slate-600/40">
        <Link
          href="/"
          className="flex items-center space-x-2 px-3 py-2 rounded-xl text-xs text-[#a9b7d0] hover:text-white hover:bg-slate-700/40 transition-colors font-medium"
        >
          <Store className="w-4 h-4 text-cyan-400" />
          <span>Back to Storefront</span>
        </Link>
      </div>
    </aside>
  );
}
