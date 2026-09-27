"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Sparkles,
  ShoppingBag,
  LayoutDashboard,
  Layers,
  History,
  ShoppingCart,
  User as UserIcon,
  ChevronDown,
  Activity,
  Search,
  Store,
  ShieldCheck,
} from "lucide-react";
import { TEST_PERSONAS } from "@/lib/api";

export default function Navbar() {
  const pathname = usePathname();
  const [currentUserId, setCurrentUserId] = useState("0");
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    const savedUser = localStorage.getItem("current_user_id") || "0";
    setCurrentUserId(savedUser);

    const updateCart = () => {
      const cart = JSON.parse(localStorage.getItem("reco_cart") || "[]");
      setCartCount(cart.length);
    };
    updateCart();
    window.addEventListener("cart_updated", updateCart);
    return () => window.removeEventListener("cart_updated", updateCart);
  }, []);

  const handleUserChange = (id: string) => {
    setCurrentUserId(id);
    localStorage.setItem("current_user_id", id);
    window.dispatchEvent(new CustomEvent("user_switched", { detail: id }));
  };

  const currentPersona = TEST_PERSONAS.find((p) => p.id === currentUserId) || TEST_PERSONAS[0];
  const isDashboard = pathname.startsWith("/dashboard");

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200/90 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-6">
          <Link href={isDashboard ? "/dashboard" : "/"} className="flex items-center space-x-3 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#1dc4e9] via-[#8594e8] to-[#a389d4] flex items-center justify-center shadow-md shadow-cyan-500/20 group-hover:scale-105 transition-transform text-white font-black text-lg">
              R
            </div>
            <div>
              <div className="font-black text-base tracking-tight text-slate-900 leading-tight">
                Recommendation<span className="text-cyan-600">OS</span>
              </div>
              <div className="text-[10px] text-slate-500 font-mono tracking-wider uppercase font-semibold">
                {isDashboard ? "Admin & MLOps Console" : "Customer Storefront"}
              </div>
            </div>
          </Link>

          {/* Navigation Links (Storefront only) */}
          {!isDashboard ? (
            <nav className="hidden md:flex items-center space-x-1">
              <Link
                href="/"
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  pathname === "/"
                    ? "bg-cyan-50 text-cyan-700 border border-cyan-200"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                Storefront
              </Link>
              <Link
                href="/products"
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  pathname === "/products"
                    ? "bg-cyan-50 text-cyan-700 border border-cyan-200"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                Catalog (500 Items)
              </Link>
              <Link
                href="/recommendations"
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center space-x-1.5 ${
                  pathname === "/recommendations"
                    ? "bg-cyan-50 text-cyan-700 border border-cyan-200"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                <Sparkles className="w-3.5 h-3.5 text-cyan-600" />
                <span>For You</span>
              </Link>
              <Link
                href="/history"
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  pathname === "/history"
                    ? "bg-cyan-50 text-cyan-700 border border-cyan-200"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                Live Telemetry
              </Link>
            </nav>
          ) : (
            <div className="hidden lg:flex items-center space-x-2 text-xs font-bold text-slate-500">
              <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200 font-mono text-[10px]">
                Org: org_flowzora_prod
              </span>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-mono text-[10px]">
                Model: two_tower_v2
              </span>
            </div>
          )}
        </div>

        {/* Right Section: Persona Selector, Cart, Dashboard Toggle */}
        <div className="flex items-center space-x-3">
          {/* Persona Selector dropdown */}
          <div className="relative group">
            <button className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold text-slate-800 hover:border-cyan-500 transition-all shadow-sm">
              <span className="text-sm">{currentPersona.avatar}</span>
              <span className="hidden sm:inline font-bold">{currentPersona.name}</span>
              <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
            </button>
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-slate-200 p-2.5 hidden group-hover:block transition-all z-50">
              <div className="text-[10px] font-bold text-slate-400 px-2 py-1 uppercase tracking-wider">
                Simulate Persona Interaction
              </div>
              {TEST_PERSONAS.map((p) => (
                <button
                  key={p.id}
                  onClick={() => handleUserChange(p.id)}
                  className={`w-full text-left flex items-start space-x-2.5 px-3 py-2 rounded-xl text-xs transition-all ${
                    currentUserId === p.id
                      ? "bg-cyan-50 text-cyan-800 border border-cyan-200 font-bold"
                      : "hover:bg-slate-50 text-slate-700"
                  }`}
                >
                  <span className="text-base">{p.avatar}</span>
                  <div>
                    <div className="font-bold text-slate-900">{p.name}</div>
                    <div className="text-[10px] text-slate-500 leading-tight">{p.segment}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Cart Icon (Show only on Storefront) */}
          {!isDashboard && (
            <Link
              href="/cart"
              className="relative p-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 hover:text-cyan-600 hover:border-cyan-500 transition-all shadow-sm"
            >
              <ShoppingCart className="w-4 h-4" />
              {cartCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] text-white text-[10px] font-black w-4 h-4 rounded-full flex items-center justify-center shadow-md">
                  {cartCount}
                </span>
              )}
            </Link>
          )}

          {/* Context Switcher Button */}
          <Link
            href={isDashboard ? "/" : "/dashboard"}
            className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white text-xs font-bold shadow-md shadow-cyan-500/20 transition-all"
          >
            {isDashboard ? (
              <>
                <Store className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Back to Storefront</span>
              </>
            ) : (
              <>
                <LayoutDashboard className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Admin Dashboard</span>
              </>
            )}
          </Link>
        </div>
      </div>
    </header>
  );
}
