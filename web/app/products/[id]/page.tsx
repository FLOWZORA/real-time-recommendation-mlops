"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  Star,
  ShoppingCart,
  Zap,
  ArrowLeft,
  Sparkles,
  ShieldCheck,
  Truck,
  RotateCcw,
  Check,
} from "lucide-react";
import ProductCard from "@/components/ProductCard";
import {
  getProductById,
  getSimilarProducts,
  sendEvent,
  Product,
  RecommendationItem,
} from "@/lib/api";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const productId = params?.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [similarItems, setSimilarItems] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [added, setAdded] = useState(false);

  const currentUserId = typeof window !== "undefined" ? localStorage.getItem("current_user_id") || "0" : "0";

  useEffect(() => {
    if (!productId) return;

    const loadData = async () => {
      setLoading(true);
      try {
        const prod = await getProductById(productId);
        setProduct(prod);

        // Record product_view event
        sendEvent(currentUserId, prod.item_id_numeric, "product_view").catch(() => {});

        // Fetch similar items via Item-to-Item embedding search
        const sim = await getSimilarProducts(prod.item_id_numeric).catch(() => []);
        setSimilarItems(sim);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [productId]);

  const handleAddToCart = () => {
    if (!product) return;
    sendEvent(currentUserId, product.item_id_numeric, "add_to_cart").catch(() => {});

    const currentCart = JSON.parse(localStorage.getItem("reco_cart") || "[]");
    currentCart.push({
      item_id: product.item_id_numeric,
      title: product.title,
      price: product.price,
      image_url: product.image_url,
    });
    localStorage.setItem("reco_cart", JSON.stringify(currentCart));
    window.dispatchEvent(new Event("cart_updated"));

    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const handleBuyNow = () => {
    if (!product) return;
    // Send purchase event immediately
    sendEvent(currentUserId, product.item_id_numeric, "purchase").catch(() => {});
    handleAddToCart();
    router.push("/cart");
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-400">
        <div className="w-10 h-10 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-xs">Loading product details and calculating vector similarities...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-400">
        <p>Product not found.</p>
        <Link href="/products" className="text-cyan-400 text-xs mt-2 inline-block">
          &larr; Back to Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Back button */}
      <Link
        href="/products"
        className="inline-flex items-center space-x-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Products</span>
      </Link>

      {/* Main Product Layout */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200/90 shadow-sm grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
        {/* Left: Gallery */}
        <div className="space-y-4">
          <div className="aspect-square rounded-2xl overflow-hidden bg-slate-50 border border-slate-200 flex items-center justify-center p-8">
            <img
              src={product.image_url || `https://picsum.photos/seed/${product.item_id_numeric}/600/600`}
              alt={product.title}
              className="w-full h-full object-contain"
            />
          </div>
        </div>

        {/* Right: Info & Actions */}
        <div className="space-y-6 flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-cyan-50 text-cyan-700 border border-cyan-200">
                Item #{product.item_id_numeric}
              </span>
              {product.badge && (
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
                  {product.badge}
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-snug">
              {product.title}
            </h1>

            <div className="flex items-center space-x-3 pt-1">
              <div className="flex items-center space-x-1 text-amber-500 text-sm font-bold">
                <Star className="w-4 h-4 fill-amber-400" />
                <span>{product.rating.toFixed(1)}</span>
              </div>
              <span className="text-slate-300">&bull;</span>
              <span className="text-xs text-slate-500 font-medium">{product.reviews_count} verified reviews</span>
            </div>

            <div className="text-3xl font-black text-slate-900 pt-2">
              ${product.price.toFixed(2)}
            </div>

            <p className="text-sm text-slate-600 leading-relaxed pt-1">
              {product.description ||
                "Engineered for audiophiles and power creators requiring state-of-the-art responsiveness, precision calibration, and zero latency."}
            </p>
          </div>

          <div className="space-y-5 pt-4">
            {/* Action CTAs */}
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleAddToCart}
                className={`flex-1 py-3 px-6 rounded-xl font-bold text-xs flex items-center justify-center space-x-2 transition-all shadow-sm ${
                  added
                    ? "bg-emerald-600 text-white"
                    : "bg-slate-900 hover:bg-slate-800 text-white"
                }`}
              >
                {added ? <Check className="w-4 h-4" /> : <ShoppingCart className="w-4 h-4" />}
                <span>{added ? "Added to Cart" : "Add to Cart"}</span>
              </button>

              <button
                onClick={handleBuyNow}
                className="flex-1 py-3 px-6 rounded-xl font-extrabold text-xs bg-gradient-to-r from-[#1dc4e9] to-[#a389d4] hover:opacity-95 text-white shadow-md shadow-cyan-500/20 flex items-center justify-center space-x-2 transition-all"
              >
                <Zap className="w-4 h-4 fill-white" />
                <span>Instant Buy Now</span>
              </button>
            </div>

            {/* Value Props */}
            <div className="pt-4 border-t border-slate-100 grid grid-cols-3 gap-4 text-[11px] text-slate-600 font-medium">
              <div className="flex items-center space-x-1.5">
                <Truck className="w-4 h-4 text-cyan-600 shrink-0" />
                <span>Next-Day Delivery</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>2-Year Warranty</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <RotateCcw className="w-4 h-4 text-indigo-600 shrink-0" />
                <span>30-Day Returns</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Similar Products (Item-to-Item Vector ANN) */}
      <section className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-cyan-600" />
            <h2 className="text-xl font-black text-slate-900">Similar Products (Item-to-Item ANN)</h2>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            Powered by 32-dim Item Tower Embeddings
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
          {similarItems.map((item) => (
            <ProductCard key={item.item_id} product={item} showScore={true} />
          ))}
        </div>
      </section>
    </div>
  );
}
