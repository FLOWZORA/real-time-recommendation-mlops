import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON
from api.database import Base

class RecommendationRequest(Base):
    __tablename__ = "recommendation_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    model_version = Column(String(100), nullable=False)
    strategy = Column(String(50), nullable=False)  # two_tower_milvus, popular_fallback, category_fallback
    latency_ms = Column(Float, nullable=False)
    cold_start = Column(Boolean, default=False, nullable=False)
    cache_hit = Column(Boolean, default=False, nullable=False)
    item_ids_served = Column(JSON, nullable=False)  # List of int item IDs
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
