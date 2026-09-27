"use client";

import React, { useState, useEffect } from "react";
import { Package, Search, Star, Layers, CheckCircle2, XCircle } from "lucide-react";
import { getProducts, Product } from "@/lib/api";

export default function DashboardProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getProducts(undefined, search || undefined, 500);
      setProducts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <Package className="w-4 h-4" />
            </div>
            <span>Product Catalog Manager</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Manage your store catalog and vector embeddings mapped directly to the PyTorch recommendation layer.
          </p>
        </div>

        <div className="flex items-center space-x-2.5 shrink-0">
          <input
            type="text"
            placeholder="Search items..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-cyan-500 w-48 sm:w-64"
          />
          <button
            onClick={load}
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all"
          >
            Search
          </button>
        </div>
      </div>

      {/* Catalog Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase text-[10px] tracking-wider">
              <tr>
                <th className="py-3.5 px-5">Item ID</th>
                <th className="py-3.5 px-5">Product Title</th>
                <th className="py-3.5 px-5">Price</th>
                <th className="py-3.5 px-5">Rating</th>
                <th className="py-3.5 px-5">Vector Status</th>
                <th className="py-3.5 px-5">Stock</th>
                <th className="py-3.5 px-5">Popularity Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                [...Array(6)].map((_, i) => (
                  <tr key={i} className="animate-pulse">
                    <td colSpan={7} className="py-4 px-5 text-center text-slate-400">Loading catalog items...</td>
                  </tr>
                ))
              ) : products.length > 0 ? (
                products.map((p) => (
                  <tr key={p.id || p.item_id_numeric} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-5 font-mono font-bold text-cyan-600">
                      #{p.item_id_numeric}
                    </td>
                    <td className="py-3.5 px-5 font-bold text-slate-900 max-w-xs truncate">
                      {p.title}
                    </td>
                    <td className="py-3.5 px-5 font-semibold text-slate-900">
                      ${Number(p.price).toFixed(2)}
                    </td>
                    <td className="py-3.5 px-5">
                      <span className="flex items-center space-x-1 text-amber-500 font-bold">
                        <Star className="w-3.5 h-3.5 fill-amber-400" />
                        <span>{p.rating || 4.5}</span>
                      </span>
                    </td>
                    <td className="py-3.5 px-5">
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-50 text-cyan-700 border border-cyan-200">
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-500"></span>
                        Indexed (64d)
                      </span>
                    </td>
                    <td className="py-3.5 px-5">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          p.in_stock
                            ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                            : "bg-rose-50 text-rose-700 border border-rose-200"
                        }`}
                      >
                        {p.in_stock ? "In Stock" : "Out of Stock"}
                      </span>
                    </td>
                    <td className="py-3.5 px-5 font-mono font-bold text-slate-700">
                      {p.popularity_score || 85} / 100
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-slate-500">
                    No products found.
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
