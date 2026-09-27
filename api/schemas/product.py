from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    icon: Optional[str] = "📦"
    color: Optional[str] = "#6366f1"

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    rating: Optional[float] = 5.0
    badge: Optional[str] = None
    image_url: Optional[str] = None
    in_stock: Optional[bool] = True
    category_id: Optional[str] = None

class ProductCreate(ProductBase):
    item_id_numeric: Optional[int] = None

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    badge: Optional[str] = None
    image_url: Optional[str] = None
    in_stock: Optional[bool] = None
    category_id: Optional[str] = None

class ProductResponse(ProductBase):
    id: str
    organization_id: str
    item_id_numeric: int
    reviews_count: int
    popularity_score: int
    created_at: datetime

    class Config:
        from_attributes = True
