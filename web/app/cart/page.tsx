"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ShoppingCart, Trash2, ArrowRight, CheckCircle2, Sparkles } from "lucide-react";
import { sendEvent } from "@/lib/api";
import { getProductImageUrl } from "@/lib/productImage";

export default function CartPage() {
  const [cart, setCart] = useState<any[]>([]);
  const [checkingOut, setCheckingOut] = useState(false);
  const [completed, setCompleted] = useState(false);

  const currentUserId = typeof window !== "undefined" ? localStorage.getItem("current_user_id") || "0" : "0";

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("reco_cart") || "[]");
    setCart(saved);
  }, []);

  const handleRemove = (index: number) => {
    const updated = [...cart];
    updated.splice(index, 1);
    setCart(updated);
    localStorage.setItem("reco_cart", JSON.stringify(updated));
    window.dispatchEvent(new Event("cart_updated"));
  };

  const handleCheckout = async () => {
    setCheckingOut(true);
    try {
      // Send purchase events for every product in cart
      for (const item of cart) {
        await sendEvent(currentUserId, item.item_id, "purchase", {
          price: item.price,
          checkout_timestamp: new Date().toISOString(),
        });
      }

      // Clear cart
      localStorage.setItem("reco_cart", "[]");
      setCart([]);
      window.dispatchEvent(new Event("cart_updated"));
      setCompleted(true);
    } catch (e) {
      console.error(e);
    } finally {
      setCheckingOut(false);
    }
  };

  const total = cart.reduce((sum, item) => sum + (item.price || 0), 0);

  if (completed) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-6">
        <div className="w-16 h-16 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto border border-emerald-200 shadow-sm">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Purchase Successful!</h1>
        <p className="text-sm text-slate-600 max-w-md mx-auto leading-relaxed">
          Your purchase event was ingested via FastAPI, published to the Kafka streaming pipeline,
          recorded in Feast online store, and triggered an online SGD model weight update.
        </p>
        <div className="pt-4 flex justify-center space-x-3">
          <Link
            href="/recommendations"
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] text-white font-bold text-xs flex items-center space-x-2 shadow-md shadow-cyan-500/20"
          >
            <Sparkles className="w-4 h-4" />
            <span>See Updated Recommendations</span>
          </Link>
          <Link
            href="/products"
            className="px-5 py-2.5 rounded-xl bg-white border border-slate-200 text-slate-800 hover:border-cyan-500 text-xs font-bold shadow-sm transition-all"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <ShoppingCart className="w-4 h-4" />
            </div>
            <span>Shopping Cart</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Review items and trigger real-time purchase feedback events.
          </p>
        </div>
      </div>

      {cart.length === 0 ? (
        <div className="bg-white p-12 rounded-2xl text-center space-y-4 border border-slate-200/90 shadow-sm">
          <ShoppingCart className="w-12 h-12 text-slate-400 mx-auto" />
          <h2 className="text-base font-bold text-slate-900">Your cart is empty</h2>
          <p className="text-xs text-slate-500">
            Browse the product catalog or recommended items to add gear to your cart.
          </p>
          <Link
            href="/products"
            className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all"
          >
            <span>Explore Catalog</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="md:col-span-2 space-y-3">
            {cart.map((item, idx) => (
              <div
                key={idx}
                className="bg-white p-4 rounded-2xl flex items-center justify-between border border-slate-200/90 shadow-sm space-x-4"
              >
                <div className="w-16 h-16 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0 border border-slate-200">
                  <img
                    src={getProductImageUrl(item.image_url, item.title, undefined, item.item_id)}
                    alt={item.title}
                    className="w-full h-full object-cover"
                  />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="text-xs font-mono font-bold text-cyan-600">Item #{item.item_id}</div>
                  <h3 className="text-sm font-bold text-slate-900 truncate">{item.title}</h3>
                  <div className="text-sm font-black text-slate-900 mt-1">
                    ${item.price?.toFixed(2)}
                  </div>
                </div>

                <button
                  onClick={() => handleRemove(idx)}
                  className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Order Summary */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-6 h-fit">
            <h2 className="text-base font-bold text-slate-900">Order Summary</h2>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between text-slate-600 font-medium">
                <span>Subtotal ({cart.length} items)</span>
                <span className="text-slate-900 font-bold">${total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-600 font-medium">
                <span>Estimated Shipping</span>
                <span className="text-emerald-700 font-bold">FREE</span>
              </div>
              <div className="pt-3 border-t border-slate-200 flex justify-between text-base font-black text-slate-900">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>

            <button
              onClick={handleCheckout}
              disabled={checkingOut}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white font-extrabold text-xs shadow-md shadow-cyan-500/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              <span>{checkingOut ? "Processing Purchase..." : "Confirm & Trigger MLOps Event"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
