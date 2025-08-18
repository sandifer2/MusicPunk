from sqlalchemy import Column, Index, CheckConstraint, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class TokenTransaction(Base):
    __tablename__ = "token_transactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # positive=earned, negative=spent
    balance_after = Column(Integer, nullable=False)
    
    # What triggered this transaction
    transaction_type = Column(String(50), nullable=False)  # 'review_posted', 'content_unlocked'
    
    # Optional reference to the thing that caused it
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=True)
    unlocked_item_id = Column(Integer, ForeignKey("unlocked_items.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    idempotency_key = Column(String(64), nullable=True, unique=True, index=True)
    
    user = relationship("User", back_populates="token_transactions")
    
    __table_args__ = (
        CheckConstraint('amount != 0', name='check_amount_not_zero'),
        Index('idx_token_trans_user_date', 'user_id', 'created_at'),
        Index('idx_token_trans_idempotency', 'idempotency_key', 'user_id'),
    )