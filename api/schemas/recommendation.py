from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class RecommendationItem(BaseModel):
    item_id: int
    title: str
    category: str
    price: float
    rating: float
    badge: Optional[str] = None
    image_url: Optional[str] = None
    in_stock: bool = True
    score: float
    relevance_score: Optional[float] = None
    popularity: Optional[int] = None
    recency: Optional[float] = None
    rank: int
    source: str = "two_tower_retrieval"
    reason: Optional[str] = None

class RecommendationResponse(BaseModel):
    user_id: str
    organization_id: str
    cold_start: bool
    strategy: str  # two_tower_milvus, popular_fallback, category_fallback, cache_fallback
    model_version: str
    variant: Optional[str] = "control"
    latency_ms: float
    cache_hit: bool = False
    recommendations: List[int]
    detailed_recommendations: List[RecommendationItem]
    user_features: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
