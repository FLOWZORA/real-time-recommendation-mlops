"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Star, ShoppingCart, Heart, Check, Sparkles } from "lucide-react";
import { sendEvent, Product, RecommendationItem } from "@/lib/api";

interface ProductCardProps {
  product: Product | RecommendationItem;
  showScore?: boolean;
}

export default function ProductCard({ product, showScore = false }: ProductCardProps) {
  const [added, setAdded] = useState(false);
  const [liked, setLiked] = useState(false);

  const itemId = "item_id_numeric" in product ? product.item_id_numeric : product.item_id;
  const currentUserId = typeof window !== "undefined" ? localStorage.getItem("current_user_id") || "0" : "0";

  const handleCardClick = () => {
    sendEvent(currentUserId, itemId, "product_click").catch(() => {});
  };

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    sendEvent(currentUserId, itemId, "add_to_cart").catch(() => {});

    const currentCart = JSON.parse(localStorage.getItem("reco_cart") || "[]");
    currentCart.push({
      item_id: itemId,
      title: product.title,
      price: product.price,
      image_url: product.image_url,
    });
    localStorage.setItem("reco_cart", JSON.stringify(currentCart));
    window.dispatchEvent(new Event("cart_updated"));

    setAdded(true);
    setTimeout(() => setAdded(false), 1500);
  };

  const handleLike = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    sendEvent(currentUserId, itemId, "product_click", { intent: "like" }).catch(() => {});
    setLiked(!liked);
  };

  return (
    <div
      onClick={handleCardClick}
      className="datta-card overflow-hidden flex flex-col group relative bg-white dark:bg-[#2b2c2f]"
    >
      {/* Top Accent Bar on Hover */}
      <div className="h-1 bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] opacity-0 group-hover:opacity-100 transition-opacity"></div>

      {/* Score Badge (if recommendation) */}
      {showScore && "score" in product && (
        <div className="absolute top-3 left-3 z-10">
          <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] text-white shadow-md">
            <Sparkles className="w-3 h-3" />
            <span>{((product as any).score * 100).toFixed(0)}% Neural Match</span>
          </span>
        </div>
      )}

      {/* Stock & Category Badge */}
      <div className="absolute top-3 right-3 z-10 flex items-center space-x-1">
        <button
          onClick={handleLike}
          className="p-1.5 rounded-full bg-white/90 dark:bg-slate-800/90 hover:bg-white text-slate-400 hover:text-rose-500 shadow-sm transition-all"
        >
          <Heart className={`w-3.5 h-3.5 ${liked ? "fill-rose-500 text-rose-500" : ""}`} />
        </button>
      </div>

      {/* Image Container */}
      <Link href={`/products/${itemId}`} className="block relative aspect-square overflow-hidden bg-slate-50 dark:bg-slate-800/40 p-6 flex items-center justify-center">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-24 h-24 rounded-2xl bg-gradient-to-tr from-cyan-50 to-indigo-50 dark:from-slate-800 dark:to-slate-700 flex items-center justify-center text-cyan-600 dark:text-cyan-400 font-black text-2xl">
            #{itemId}
          </div>
        )}
      </Link>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        <div>
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-600 mb-1">
            <span className="uppercase tracking-wide">{"category" in product ? (product as any).category : "Electronics"}</span>
            <span className="flex items-center space-x-1 text-amber-600 font-black">
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-500" />
              <span>{product.rating ? Number(product.rating).toFixed(1) : "4.8"}</span>
            </span>
          </div>

          <Link href={`/products/${itemId}`}>
            <h3 className="text-xs font-bold text-slate-900 group-hover:text-cyan-600 transition-colors line-clamp-2 leading-relaxed">
              {product.title}
            </h3>
          </Link>
        </div>

        {/* Price & Add to Cart Action */}
        <div className="flex items-center justify-between pt-2.5 border-t border-slate-200/80">
          <div>
            <div className="text-[10px] text-slate-500 uppercase font-mono font-bold">Price</div>
            <div className="text-sm font-black text-slate-900">
              ${Number(product.price).toFixed(2)}
            </div>
          </div>

          <button
            onClick={handleAddToCart}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center space-x-1.5 transition-all shadow-sm ${
              added
                ? "bg-emerald-600 text-white"
                : "bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white shadow-cyan-500/20"
            }`}
          >
            {added ? (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Added</span>
              </>
            ) : (
              <>
                <ShoppingCart className="w-3.5 h-3.5" />
                <span>Add</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
