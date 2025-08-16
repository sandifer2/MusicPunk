from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Literal, Union
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal 
import re

class TransactionType(str, Enum):

    REVIEW_POSTED = "review_posted"
    SIGNUP_BONUS = "signup_bonus"
    REFERRAL_BONUS = "referral_bonus"
    ACHIEVEMENT_EARNED = " achievement_earned"

    CONTENT_UNLOCKED = "content_unlocked"
    FEATURE_PURCHASE = "feature_purchase"

    ADMIN_GRANT = "admin_grant"
    ADMIN_DEDUCT = "admin_deduct"

    TOKEN_PURCHASE = "token_purchase"
    TOKEN_REFUND = "token_refund"


class TokenTransactionBase(BaseModel):
    amount: int = Field(..., description="Positive for credits, negative for debits")
    TransactionType = TransactionType

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True
    )

class TokenTransactionCreate(TokenTransactionBase):
    user_id: int = Field(..., gt=0)
    balance_after: Optional[int] = Field(None, gt=0)

    review_id: Optional[int] = Field(None, gt=0)
    unlocked_item_id: Optional[int] = Field(None, gt=0)

    idempotency_key: Optional[str] = Field(
        None,
        min_length=8,
        max_length=64,
        description="prevents duplicate transactions"
    )
    metadata: Optional[dict] = Field(
        None,
        description="additional context for debugging and analysis"
    )
    @field_validator('amount')
    @classmethod
    def valiadate_amount(cls, amount: int, info) -> int:
        if amount == 0:
            raise ValueError("Transaction amount cannot be zero")
        
        transaction_type = info.data.get('transaction_type')

        earning_types = { #wwd
            TransactionType.REVIEW_POSTED,
            TransactionType.SIGNUP_BONUS,
            TransactionType.REFERRAL_BONUS,
            TransactionType.ACHIEVEMENT_EARNED,
            TransactionType.ADMIN_GRANT,
            TransactionType.TOKEN_PURCHASE
        }

        spending_types = {
            TransactionType.CONTENT_UNLOCKED,
            TransactionType.FEATURE_PURCHASE,
            TransactionType.ADMIN_DEDUCT,
            TransactionType.TOKEN_REFUND
        }

        if transaction_type in earning_types and amount < 0:
            raise ValueError(f"Transaction type {transaction_type} must have a positive amount ")
        elif transaction_type in spending_types and amount > 0:
            raise ValueError(f"Transaction amount exceeds maximum allowed (100,000 tokens)")
        
        return amount
    @model_validator(mode='after')
    def validate_references(self) -> 'TokenTransactionCreate':
        if self.transaction_type == TransactionType.REVIEW_POSTED:
            if not self.review_id:
                raise ValueError("Review ID required for REVIEW_POSTED transaction")
            if self.unlocked_item_id:
                raise ValueError("Unlocked item ID should not be set for REVIEW_POSTED")
        elif self.transaction_type == TransactionType.CONTENT_UNLOCKED:
            if not self.unlocked_item_id:
                raise ValueError("Unlocked item ID required for CONTENT_UNLOCKED transaction")
            if self.review_id:
                raise ValueError("Review ID shoul dnot be set for CONTENT_UNLOCKED")
        elif self.TransactionType in{
             TransactionType.ADMIN_GRANT, 
            TransactionType.ADMIN_DEDUCT,
            TransactionType.SIGNUP_BONUS,
            TransactionType.REFERRAL_BONUS
        }: 
            if self.review or self.unlocked_item_id:
                raise ValueError(f"Transaction type {self.transaction_type} should not reference other entitites")
        return self
        
    @field_validator('idempotency_key')
    @classmethod
    def validate_idempotency_key(cls, key: Optional[str]) -> Optional[str]:
        if key is None:
            return None
        if not re.match(r'^[A-Za-z0-9_\-]+$', key):
            raise ValueError("Idempotency key must be URL safe (alphanumeric, _ or - only )")

        return key
    
class TokenTransactionResponse(TokenTransactionBase):
    id: int
    user_id: int 
    balance_after: int
    created_at: datetime

    review_id: Optional[int] = None
    unlocked_item_id: Optional[int] = None #this may not work becuase we changed our polymorphic key to multiple relationships instead

    #display
    display_descriptionL: Optional[str] = None
    is_credit: bool = Field(default=False)

    @model_validator(mode='after')
    def compute_display_fields(self) -> 'TokenTransactionResponse': #single purpose principal
        self.is_credit = self.amount > 0
        
        descriptions = {
            TransactionType.REVIEW_POSTED: f"Earned {abs(self.amount)} tokens for posting a review",
            TransactionType.SIGNUP_BONUS: f"Welcome bonus: {abs(self.amount)} tokens",
            TransactionType.CONTENT_UNLOCKED: f"Spent {abs(self.amount)} tokens to unlock content",
            TransactionType.ADMIN_GRANT: f"Granted {abs(self.amount)} tokens by admin",
            TransactionType.ADMIN_DEDUCT: f"Deducted {abs(self.amount)} tokens by admin",
            TransactionType.TOKEN_PURCHASE: f"Purchased {abs(self.amount)} tokens",
            TransactionType.TOKEN_REFUND: f"Refunded {abs(self.amount)} tokens",
        }

        self.display_description = descriptions.get(
            self.transaction_type,
            f"{'Earned' if self.is_credit else 'Spent'} {abs(self.amount)} tokens"
        )

        return self
    
class TokenBalance(BaseModel):
    user_id: int
    current_balance: int = Field(...,ge=0)
    total_earned: int = Field(..., ge=0)
    total_spent: int = Field(..., ge=0)

    recent_transactions: List[TokenTransactionResponse] = []

    earning_rate_daily: float = Field(default=0.0, description="Average tokens earned earned per day: ")
    spending_rate_daily: float = Field(default=0.0, description="Average tokens spent per day: ")
    days_until_depleted: Optional[int] = Field(None, description="Estimated days until 0 tokens: ")

    @model_validator(mode='afer')
    def calculate_analytics(self) -> 'TokenBalance':
        if self.spending_rate_daily > 0 and self.current_balance > 0:
            net_daily = self.earning_rate_daily - self.spending_rate_daily
            if net_daily < 0:
                self.days_until_depleted = int(self.current_balance / abs(net_daily))

        return self
    
class TokenTransactionHistory(BaseModel):

    transactions: List[TokenTransactionResponse]
    total_count: int
    page: int = Field(..., ge=1, le=100)
    has_next: bool
    has_prev: bool
     # just make this a general transaction history, no period needed
    

class TokenGrantRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    amount: int = Field(..., ne=0, ge=-10000, le=10000) #what does this all do
    reason: str = Field(..., min_length=3, max_length=200)
    transaction_type: Literal[TransactionType.ADMIN_GRANT, TransactionType.ADMIN_DEDUCT]

    @model_validator
    def validate_grant_type(self) -> 'TokenGrantRequest':
        if self.amount > 0 and self.transaction_type != TransactionType.ADMIN_GRANT:
            self.transaction_type = TransactionType.ADMIN_GRANT
        if self.amount < 0 and self.transaction_type != TransactionType.ADMIN_DEDUCT:
            self.transaction_type = TransactionType.ADMIN_DEDUCT

        return self