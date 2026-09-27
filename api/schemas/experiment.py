from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class ExperimentCreate(BaseModel):
    name: str
    variant_a_model: str = "TwoTowerRecommender:Production"
    variant_b_model: str = "TwoTowerRecommender:Staging"
    traffic_split_b: float = 0.2

class ExperimentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None  # ACTIVE, PAUSED, CONCLUDED
    traffic_split_b: Optional[float] = None

class ExperimentResponse(BaseModel):
    id: str
    name: str
    status: str
    variant_a_model: str
    variant_b_model: str
    traffic_split_b: float
    total_assignments: Optional[int] = 0
    variant_a_impressions: Optional[int] = 0
    variant_b_impressions: Optional[int] = 0
    variant_a_clicks: Optional[int] = 0
    variant_b_clicks: Optional[int] = 0
    variant_a_ctr: Optional[float] = 0.0
    variant_b_ctr: Optional[float] = 0.0
    statistically_significant: Optional[bool] = False
    p_value: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ModelDeployRequest(BaseModel):
    model_name: str = "TwoTowerRecommender"
    version: str
    target_stage: str = "Production"  # Staging, Canary, Production, Archived

class ModelVersionResponse(BaseModel):
    name: str
    version: str
    stage: str
    run_id: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

class AnalyticsOverviewResponse(BaseModel):
    total_products: int
    total_users: int
    total_events: int
    recommendation_requests_today: int
    avg_latency_ms: float
    overall_ctr: float
    conversion_rate: float
    cold_start_rate: float
    cache_hit_rate: float
    active_experiments: int
    current_model: str
