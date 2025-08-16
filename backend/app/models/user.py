from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True,  nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(512), nullable=False)
    tokens = Column(Integer, default=100, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    unlocked_items = relationship("UnlockedItem", back_populates="user", cascade="all, delete-orphan")
    token_transactions = relationship("TokenTransaction", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (CheckConstraint('tokens >= 0', name='check_tokens_non_negative'),)

