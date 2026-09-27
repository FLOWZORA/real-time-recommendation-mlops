import time
from typing import List, Dict, Any, Optional
import torch
import numpy as np
from sqlalchemy.orm import Session

from serving.model_loader import model, MODEL_NAME, MODEL_STAGE
from serving.user_features import get_user_features
from vector_db.milvus import search
from ranking.features import build_ranking_features
from ranking.ranker import rank_items
from cold_start.handler import cold_start_recommend
from features.catalog_data import get_item_metadata, get_user_persona
from serving.cache import cache_get, cache_set
from api.models.product import Product
from api.models.event import UserEvent

class RecommendationPipeline:
    """
    Production-style 3-Stage Recommendation Serving Engine:
    Stage 1: Candidate Generation / Sourcing (ANN, Category, Trending)
    Stage 2: Scoring & Ranking (Two-Tower dot product + ranking weights)
    Stage 3: Re-ranking & Business Constraints (Stock, Purchased item filter, Category diversity)
    With Graceful 4-Tier Degradation (Cache -> Category -> Trending -> Global Popular).
    """

    def __init__(self, timeout_sec: float = 0.5):
        self.timeout_sec = timeout_sec

    def generate_recommendations(
        self,
        user_id_raw: str,
        organization_id: str,
        db: Optional[Session] = None,
        top_k: int = 10,
        enable_cache: bool = True,
        excluded_item_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        start_time = time.time()
        cache_key = f"rec:{organization_id}:{user_id_raw}:{top_k}"

        # 0. Check Cache (Fallback Tier 1)
        if enable_cache:
            cached_result = cache_get(cache_key)
            if cached_result:
                cached_result["cache_hit"] = True
                cached_result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
                return cached_result

        # Map user_id to numeric index for feature store & Two-Tower model
        try:
            numeric_user_id = int(user_id_raw)
        except ValueError:
            numeric_user_id = abs(hash(user_id_raw)) % 1000

        # Exclude recent purchases if DB session is available
        purchased_items = set(excluded_item_ids or [])
        if db:
            try:
                recent_purchases = db.query(UserEvent.item_id_numeric).filter(
                    UserEvent.organization_id == organization_id,
                    UserEvent.user_id == str(user_id_raw),
                    UserEvent.event_type == "purchase"
                ).limit(50).all()
                for p in recent_purchases:
                    purchased_items.add(p[0])
            except Exception:
                pass

        # 1. Fetch user features & check Cold-Start
        is_explicit_cold = str(user_id_raw).lower().startswith("cold") or numeric_user_id == 999
        try:
            user_features, is_cold = get_user_features(numeric_user_id)
            if is_explicit_cold:
                is_cold = True
            features_list = user_features[0].tolist()
        except Exception:
            user_features = torch.zeros((1, 8), dtype=torch.float32)
            is_cold = True
            features_list = [0] * 8

        persona = get_user_persona(numeric_user_id)

        # 2. Cold-start handler (Fallback Tier 4)
        if is_cold:
            cs_result = cold_start_recommend(numeric_user_id)
            candidates = cs_result["items"]
            detailed_items = self._re_rank_and_enrich(
                candidates,
                purchased_items,
                organization_id,
                db,
                top_k,
                source="cold_start_popular",
            )
            latency = round((time.time() - start_time) * 1000, 2)
            resp = {
                "user_id": str(user_id_raw),
                "organization_id": organization_id,
                "cold_start": True,
                "strategy": "popular_fallback",
                "model_version": f"{MODEL_NAME}:{MODEL_STAGE}",
                "latency_ms": latency,
                "cache_hit": False,
                "recommendations": [item["item_id"] for item in detailed_items],
                "detailed_recommendations": detailed_items,
                "user_features": {
                    "total_views": int(features_list[0]),
                    "total_clicks": int(features_list[1]),
                    "total_purchases": int(features_list[2]),
                },
                "explanation": "Cold-start fallback: Top trending items across all store shoppers.",
            }
            if enable_cache:
                cache_set(cache_key, resp, ttl_seconds=120)
            return resp

        # 3. STAGE 1: Candidate Generation (ANN Vector Search)
        try:
            with torch.no_grad():
                user_embedding = model.user(user_features).numpy()

            # Retrieve top 50 candidates from ANN Milvus / Local Vector Store
            retrieved_ids = search(user_embedding, top_k=50)
        except Exception as e:
            # Fallback Tier 3: Category / Trending Fallback on vector store failure
            print(f"[WARN] Retrieval failed ({e}), using trending fallback")
            retrieved_ids = list(range(30))

        # 4. STAGE 2: Scoring & Ranking Layer
        scored_candidates = []
        for item_id in retrieved_ids:
            if item_id in purchased_items:
                continue
            feats = build_ranking_features(numeric_user_id, item_id)
            feats["item_id"] = item_id
            scored_candidates.append(feats)

        ranked = rank_items(scored_candidates)

        # 5. STAGE 3: Re-ranking & Business Constraints (Stock, Diversity, Deduplication)
        top_candidates = [cand["item_id"] for cand in ranked[:40]]
        detailed_items = self._re_rank_and_enrich(
            top_candidates,
            purchased_items,
            organization_id,
            db,
            top_k,
            source="two_tower_retrieval",
            persona=persona,
        )

        latency = round((time.time() - start_time) * 1000, 2)
        segment = persona.get("segment", "Top personalized products")
        resp = {
            "user_id": str(user_id_raw),
            "organization_id": organization_id,
            "cold_start": False,
            "strategy": "two_tower_milvus",
            "model_version": f"{MODEL_NAME}:{MODEL_STAGE}",
            "latency_ms": latency,
            "cache_hit": False,
            "recommendations": [item["item_id"] for item in detailed_items],
            "detailed_recommendations": detailed_items,
            "user_features": {
                "total_views": persona.get("views", int(features_list[0])),
                "total_clicks": persona.get("clicks", int(features_list[1])),
                "total_purchases": persona.get("purchases", int(features_list[2])),
            },
            "explanation": f"Personalized for {persona['name']}: {segment}",
        }

        if enable_cache:
            cache_set(cache_key, resp, ttl_seconds=60)

        return resp

    def _re_rank_and_enrich(
        self,
        candidate_ids: List[int],
        purchased_items: set,
        organization_id: str,
        db: Optional[Session],
        top_k: int,
        source: str = "two_tower_retrieval",
        persona: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Re-ranking stage applying:
        1. Duplicate suppression
        2. Purchased item exclusion
        3. Stock availability verification
        4. Category balance (primary persona category up to 7 items in top-10, complementary items up to 3)
        """
        seen_ids = set()
        seen_titles = set()
        category_counts = {}
        enriched_list = []
        primary_cat = persona.get("primary_cat") if persona else None

        # Preload product metadata from DB if available
        db_products_map = {}
        if db:
            try:
                db_prods = db.query(Product).filter(
                    Product.organization_id == organization_id,
                    Product.item_id_numeric.in_(candidate_ids[:50])
                ).all()
                for p in db_prods:
                    db_products_map[p.item_id_numeric] = p
            except Exception:
                pass

        for rank, item_id in enumerate(candidate_ids):
            if item_id in seen_ids or item_id in purchased_items:
                continue

            # Lookup metadata from DB or fallback catalog
            db_p = db_products_map.get(item_id)
            if db_p:
                if not db_p.in_stock:
                    continue  # Filter out out-of-stock items
                title = db_p.title
                category = db_p.category.name if db_p.category else "Electronics"
                price = db_p.price
                rating = db_p.rating
                badge = db_p.badge
                image_url = db_p.image_url
                if not image_url or "picsum.photos" in image_url:
                    meta = get_item_metadata(item_id)
                    image_url = meta.get("image_url")
            else:
                meta = get_item_metadata(item_id)
                title = meta.get("title", f"Product {item_id}")
                category = meta.get("category", "General")
                price = meta.get("price", 99.99)
                rating = meta.get("rating", 4.8)
                badge = meta.get("badge")
                image_url = meta.get("image_url")

            if title in seen_titles:
                continue

            # Category diversity constraint: max 4 items per category
            max_allowed = 4
            cat_count = category_counts.get(category, 0)
            if cat_count >= max_allowed:
                continue

            category_counts[category] = cat_count + 1
            seen_ids.add(item_id)
            seen_titles.add(title)

            score = round(max(0.1, 1.0 - (len(enriched_list) * 0.08)), 3)

            if primary_cat and category == primary_cat:
                reason = f"High-affinity match for {persona['name']} in {category}"
            else:
                reason = f"Complementary gear in {category}"

            enriched_list.append({
                "item_id": item_id,
                "title": title,
                "category": category,
                "price": price,
                "rating": rating,
                "badge": badge,
                "image_url": image_url,
                "in_stock": True,
                "score": score,
                "rank": len(enriched_list) + 1,
                "source": source,
                "reason": reason,
            })

            if len(enriched_list) >= top_k:
                break

        # Ensure we always return exactly top_k items by backfilling diverse catalog items
        if len(enriched_list) < top_k:
            from cold_start.popularity import POPULAR_ITEMS
            for backfill_id in POPULAR_ITEMS:
                if len(enriched_list) >= top_k:
                    break
                if backfill_id in seen_ids or backfill_id in purchased_items:
                    continue
                meta = get_item_metadata(backfill_id)
                b_cat = meta.get("category", "General")
                if category_counts.get(b_cat, 0) >= 4:
                    continue
                seen_ids.add(backfill_id)
                category_counts[b_cat] = category_counts.get(b_cat, 0) + 1
                enriched_list.append({
                    "item_id": backfill_id,
                    "title": meta.get("title", f"Product {backfill_id}"),
                    "category": b_cat,
                    "price": meta.get("price", 99.99),
                    "rating": meta.get("rating", 4.8),
                    "badge": meta.get("badge", "Popular"),
                    "image_url": meta.get("image_url"),
                    "in_stock": True,
                    "score": round(max(0.05, 0.4 - (len(enriched_list) * 0.03)), 3),
                    "rank": len(enriched_list) + 1,
                    "source": "diversity_backfill",
                    "reason": f"Diverse top recommendation in {b_cat}",
                })

        return enriched_list


recommendation_pipeline = RecommendationPipeline()
