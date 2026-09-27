from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    user_id: str
    item_id: int = Field(..., alias="item_id")
    event_type: str = Field(..., description="product_view, product_click, add_to_cart, purchase, wishlist")
    propensity: Optional[float] = 0.1
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True

class BatchEventsRequest(BaseModel):
    events: List[EventCreate]

class EventResponse(BaseModel):
    id: str
    organization_id: str
    user_id: str
    item_id_numeric: int
    event_type: str
    reward: float
    created_at: datetime

    class Config:
        from_attributes = True
