from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class AutoSaveFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AutoSaveStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class AutoSave(Base):
    __tablename__ = "auto_saves"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    is_active = Column(Boolean, default=True)
    status = Column(Enum(AutoSaveStatus), default=AutoSaveStatus.ACTIVE)
    
    # Fixed auto-save
    fixed_amount = Column(Float, nullable=True)
    frequency = Column(Enum(AutoSaveFrequency), nullable=True)
    
    # Round-up settings
    round_up_enabled = Column(Boolean, default=False)
    round_up_multiplier = Column(Integer, default=1)
    
    # Daily auto-save
    daily_auto_save_enabled = Column(Boolean, default=False)
    daily_amount = Column(Float, nullable=True)
    
    # Next execution
    next_execution_date = Column(DateTime(timezone=True))
    last_execution_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="auto_saves")
