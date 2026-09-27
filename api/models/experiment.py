import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from api.database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)  # ACTIVE, PAUSED, CONCLUDED
    variant_a_model = Column(String(100), default="TwoTowerRecommender:Production", nullable=False)
    variant_b_model = Column(String(100), default="TwoTowerRecommender:Staging", nullable=False)
    traffic_split_b = Column(Float, default=0.2, nullable=False)  # e.g. 20% to variant B
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    organization = relationship("Organization", back_populates="experiments")
    assignments = relationship("ExperimentAssignment", back_populates="experiment", cascade="all, delete-orphan")

class ExperimentAssignment(Base):
    __tablename__ = "experiment_assignments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    variant = Column(String(1), nullable=False)  # 'A' or 'B'
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    experiment = relationship("Experiment", back_populates="assignments")

    __table_args__ = (
        UniqueConstraint("experiment_id", "user_id", name="uq_exp_assignment_user"),
    )
