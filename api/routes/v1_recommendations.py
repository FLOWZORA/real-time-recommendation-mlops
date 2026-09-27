from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import numpy as np
import time

from api.database import get_db
from api.schemas.recommendation import RecommendationResponse, RecommendationItem
from api.security.permissions import get_auth_context, AuthContext
from api.models.recommendation import RecommendationRequest
from api.models.product import Product
from serving.pipeline import recommendation_pipeline
from vector_db.milvus import search, _local_embeddings
from features.catalog_data import get_item_metadata

router = APIRouter(tags=["Recommendations"])

def _log_recommendation_request(
    db_session: Session,
    org_id: str,
    user_id: str,
    resp: dict,
):
    try:
        req_record = RecommendationRequest(
            organization_id=org_id,
            user_id=str(user_id),
            model_version=resp.get("model_version", "TwoTower:Prod"),
            strategy=resp.get("strategy", "two_tower_milvus"),
            latency_ms=resp.get("latency_ms", 0.0),
            cold_start=resp.get("cold_start", False),
            cache_hit=resp.get("cache_hit", False),
            item_ids_served=resp.get("recommendations", []),
        )
        db_session.add(req_record)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"[WARN] Could not log recommendation request: {e}")

@router.get("/v1/recommendations", response_model=RecommendationResponse)
def get_recommendations_query(
    user_id: str = Query(..., description="Target user identifier (e.g. user_123 or 0)"),
    limit: int = Query(10, ge=1, le=50),
    disable_cache: bool = Query(False),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    org_id = ctx.organization_id or "demo-store"
    resp = recommendation_pipeline.generate_recommendations(
        user_id_raw=user_id,
        organization_id=org_id,
        db=db,
        top_k=limit,
        enable_cache=not disable_cache,
    )
    _log_recommendation_request(db, org_id, user_id, resp)
    return resp

@router.get("/v1/recommendations/{user_id}", response_model=RecommendationResponse)
def get_recommendations_path(
    user_id: str,
    limit: int = Query(10, ge=1, le=50),
    disable_cache: bool = Query(False),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    org_id = ctx.organization_id or "demo-store"
    resp = recommendation_pipeline.generate_recommendations(
        user_id_raw=user_id,
        organization_id=org_id,
        db=db,
        top_k=limit,
        enable_cache=not disable_cache,
    )
    _log_recommendation_request(db, org_id, user_id, resp)
    return resp

@router.get("/v1/similar/{product_id}", response_model=List[RecommendationItem])
def get_similar_products(
    product_id: str,
    limit: int = Query(6, ge=1, le=20),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    """
    Item-to-Item candidate generation using embedding similarity.
    """
    try:
        numeric_id = int(product_id)
    except ValueError:
        numeric_id = abs(hash(product_id)) % 500

    if numeric_id < 0 or numeric_id >= 500:
        numeric_id = numeric_id % 500

    # Retrieve vector embedding of the target product
    if _local_embeddings is not None and numeric_id < len(_local_embeddings):
        target_vec = _local_embeddings[numeric_id]
        # Query nearest neighbors, excluding the product itself
        candidate_ids = search(target_vec, top_k=limit + 1)
        candidate_ids = [cid for cid in candidate_ids if cid != numeric_id][:limit]
    else:
        # Fallback to category/neighboring IDs
        candidate_ids = [(numeric_id + i + 1) % 500 for i in range(limit)]

    similar_items = []
    for rank, item_id in enumerate(candidate_ids):
        meta = get_item_metadata(item_id)
        similar_items.append(RecommendationItem(
            item_id=item_id,
            title=meta.get("title", f"Product {item_id}"),
            category=meta.get("category", "General"),
            price=float(meta.get("price", 99.99)),
            rating=float(meta.get("rating", 4.8)),
            badge=meta.get("badge"),
            image_url=f"https://picsum.photos/seed/{item_id}/400/300",
            in_stock=True,
            score=round(max(0.2, 0.95 - (rank * 0.1)), 3),
            rank=rank + 1,
            source="item_to_item_ann",
            reason=f"Customers who viewed this also viewed {meta.get('category')}",
        ))

    return similar_items
