from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class KYCStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    NOT_SUBMITTED = "not_submitted"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    hashed_password = Column(String(255))
    google_id = Column(String(255), unique=True, nullable=True)
    
    # KYC Fields
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.NOT_SUBMITTED)
    pan_number = Column(String(10), unique=True, nullable=True)
    aadhaar_number = Column(String(12), unique=True, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(Text, nullable=True)
    kyc_documents = Column(JSON, default=list)
    kyc_verified_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")
    gold_holdings = relationship("GoldHolding", back_populates="user")
    auto_saves = relationship("AutoSave", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.phone}>"
