import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from api.database import Base

class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    item_id_numeric = Column(Integer, nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # product_view, product_click, add_to_cart, purchase
    propensity = Column(Float, default=0.1, nullable=False)
    reward = Column(Float, default=0.0, nullable=False)
    event_metadata = Column(JSON, default=dict, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    organization = relationship("Organization", back_populates="events")
