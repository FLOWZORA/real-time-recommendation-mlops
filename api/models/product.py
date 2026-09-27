import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from api.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    icon = Column(String(20), nullable=True)
    color = Column(String(30), nullable=True)

    products = relationship("Product", back_populates="category")

    __table_args__ = (
        UniqueConstraint("organization_id", "slug", name="uq_org_category_slug"),
    )

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id_numeric = Column(Integer, nullable=False, index=True)  # Maps to Two-Tower vector embedding (0..499)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.0, nullable=False)
    rating = Column(Float, default=5.0, nullable=False)
    reviews_count = Column(Integer, default=0, nullable=False)
    badge = Column(String(50), nullable=True)
    image_url = Column(String(500), nullable=True)
    in_stock = Column(Boolean, default=True, nullable=False)
    popularity_score = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    organization = relationship("Organization", back_populates="products")
    category = relationship("Category", back_populates="products")

    __table_args__ = (
        UniqueConstraint("organization_id", "item_id_numeric", name="uq_org_item_numeric"),
    )
