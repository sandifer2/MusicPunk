from app.core.config import settings
from app.models import User, TokenTransaction, Review
from app.schemas.token_transaction import TransactionType
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

class TokenService:
    """
    Centralized service for all token-related operations.
    This is where your token economy logic lives.
    """
    
    @staticmethod
    def calculate_review_reward(review_text: Optional[str]) -> int:
        """
        Calculate tokens earned for a review based on content.
        
        Why: Incentivize quality reviews with more tokens.
        """
        if not review_text or len(review_text) < settings.MIN_REVIEW_LENGTH:
            return settings.TOKENS_PER_REVIEW_NO_TEXT
        
        # Check for weekend bonus
        if settings.DOUBLE_TOKEN_WEEKEND and datetime.now().weekday() >= 5:
            return settings.TOKENS_PER_REVIEW * 2
            
        return settings.TOKENS_PER_REVIEW
    
    @staticmethod
    def get_signup_bonus() -> int:
        """
        Get current signup bonus amount.
        
        Why: Allows for promotional periods.
        """
        base_bonus = settings.TOKENS_SIGNUP_BONUS
        
        if settings.NEW_USER_PROMO_ACTIVE:
            return base_bonus + 50  # Extra 50 tokens during promo
            
        return base_bonus
    
    @staticmethod
    def get_unlock_cost(item_type: str) -> int:
        """
        Get unlock cost for different item types.
        
        Future: Could have different costs per type.
        """
        # For now, flat rate
        return settings.TOKENS_UNLOCK_COST
        
        # Future expansion:
        # costs = {
        #     "SONG": settings.TOKENS_UNLOCK_COST_SONG,
        #     "ALBUM": settings.TOKENS_UNLOCK_COST_ALBUM,
        #     "ARTIST": settings.TOKENS_UNLOCK_COST_ARTIST
        # }
        # return costs.get(item_type, settings.TOKENS_UNLOCK_COST)
    
    @staticmethod
    async def can_user_afford(db: Session, user_id: int, cost: int) -> bool:
        """Check if user has enough tokens."""
        user = db.query(User).filter(User.id == user_id).first()
        return user and user.tokens >= cost
    
    @staticmethod
    async def transfer_tokens(
        db: Session,
        user_id: int,
        amount: int,
        transaction_type: TransactionType,
        reference_id: Optional[int] = None,
        idempotency_key: Optional[str] = None
    ) -> TokenTransaction:
        """
        Core method to handle any token transaction.
        
        Why: Single place for all token movements with proper locking.
        """
        # Check idempotency
        if idempotency_key:
            existing = db.query(TokenTransaction).filter(
                TokenTransaction.idempotency_key == idempotency_key,
                TokenTransaction.user_id == user_id
            ).first()
            if existing:
                return existing
        
        # Lock user row to prevent race conditions
        user = db.query(User).filter(
            User.id == user_id
        ).with_for_update().first()  # Row-level lock
        
        if not user:
            raise ValueError("User not found")
        
        new_balance = user.tokens + amount
        
        if new_balance < 0:
            raise ValueError(f"Insufficient tokens. Have: {user.tokens}, Need: {abs(amount)}")
        
        # Update user balance
        user.tokens = new_balance
        
        # Create transaction record
        transaction = TokenTransaction(
            user_id=user_id,
            amount=amount,
            balance_after=new_balance,
            transaction_type=transaction_type,
            review_id=reference_id if transaction_type == TransactionType.REVIEW_POSTED else None,
            unlocked_item_id=reference_id if transaction_type == TransactionType.CONTENT_UNLOCKED else None,
            idempotency_key=idempotency_key
        )
        
        db.add(transaction)
        db.commit()
        
        return transaction