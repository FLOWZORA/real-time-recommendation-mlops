"use client";

import React, { useState, useEffect } from "react";
import { Search, Filter, ShoppingBag } from "lucide-react";
import ProductCard from "@/components/ProductCard";
import { getProducts, Product } from "@/lib/api";

const CATEGORIES = [
  "All",
  "Audio & Sound",
  "Computing & Displays",
  "Keyboards & Peripherals",
  "Creator & Studio",
  "Smart Home & Power",
  "Workspace & Lifestyle",
];

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const loadProducts = async (limit: number = 50) => {
    setLoading(true);
    try {
      const data = await getProducts(
        selectedCategory === "All" ? undefined : selectedCategory,
        searchQuery || undefined,
        limit,
        0
      );
      setProducts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = async () => {
    setLoadingMore(true);
    try {
      const more = await getProducts(
        selectedCategory === "All" ? undefined : selectedCategory,
        searchQuery || undefined,
        50,
        products.length
      );
      setProducts((prev) => [...prev, ...more]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingMore(false);
    }
  };

  const handleShowAll = async () => {
    await loadProducts(500);
  };

  useEffect(() => {
    loadProducts(50);
  }, [selectedCategory]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadProducts(50);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Title & Search Card */}
      <div className="datta-card p-6 bg-white dark:bg-[#2b2c2f] border border-slate-200/80 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 dark:bg-cyan-950/60 text-cyan-600 dark:text-cyan-400 flex items-center justify-center">
              <ShoppingBag className="w-4 h-4" />
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-800 dark:text-white tracking-tight">
              Product Catalog
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Browse all 500 catalog items with real-time vector embeddings and instant event tracking.
          </p>
        </div>

        {/* Search Input */}
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-72">
          <input
            type="text"
            placeholder="Search catalog..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded-xl text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 shadow-sm"
          />
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
        </form>
      </div>

      {/* Category Filter Chips & Count Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center space-x-2 overflow-x-auto pb-2 scrollbar-none">
          <Filter className="w-4 h-4 text-slate-400 shrink-0 mr-1" />
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all shadow-sm ${
                selectedCategory === cat
                  ? "bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] text-white shadow-cyan-500/20"
                  : "bg-white dark:bg-[#2b2c2f] text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200/80 dark:border-slate-700"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="text-xs font-mono text-slate-500 dark:text-slate-400 shrink-0">
          Showing <span className="font-bold text-cyan-600 dark:text-cyan-400">{products.length}</span> of 500 Products
        </div>
      </div>

      {/* Product Grid */}
      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="datta-card h-72 animate-pulse bg-slate-100 dark:bg-slate-800 rounded-2xl" />
          ))}
        </div>
      ) : products.length > 0 ? (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id || product.item_id_numeric} product={product} />
            ))}
          </div>

          {/* Pagination Controls */}
          {products.length < 500 && (
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-6 pb-4">
              <button
                onClick={handleLoadMore}
                disabled={loadingMore}
                className="px-5 py-2.5 rounded-xl text-xs font-bold bg-white dark:bg-[#2b2c2f] border border-slate-200 dark:border-slate-700 hover:border-cyan-500 text-slate-800 dark:text-slate-200 shadow-sm transition-all"
              >
                {loadingMore ? "Loading Next 50..." : "Load Next 50 Products"}
              </button>
              <button
                onClick={handleShowAll}
                className="px-5 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white shadow-md shadow-cyan-500/20 transition-all"
              >
                Load All 500 Products
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="datta-card text-center py-16 p-6">
          <p className="text-slate-500 text-sm">No products found matching your filter.</p>
        </div>
      )}
    </div>
  );
}
