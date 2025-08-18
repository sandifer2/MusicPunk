from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Literal, Union
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal 
from core.config import settings
import re

class TransactionType(str, Enum):

    REVIEW_POSTED = "review_posted"
    SIGNUP_BONUS = "signup_bonus"
    CONTENT_UNLOCKED = "content_unlocked"
    
class TokenTransactionBase(BaseModel):
    amount: int = Field(..., description="Positive for credits, negative for debits")
    TransactionType: TransactionType

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True
    )

class TokenTransactionCreate(TokenTransactionBase):
    user_id: int = Field(..., gt=0)
    balance_after: Optional[int] = Field(None, ge=0)

    review_id: Optional[int] = Field(None, gt=0)
    unlocked_item_id: Optional[int] = Field(None, gt=0)

    idempotency_key: Optional[str] = Field(
        None,
        min_length=8,
        max_length=64,
        description="prevents duplicate transactions"
    )

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, amount: int, info) -> int:
        if amount == 0:
            raise ValueError("Transaction amount cannot be zero")
        
        transaction_type = info.data.get('transaction_type')

        earning_types = { 
            TransactionType.REVIEW_POSTED,
            TransactionType.SIGNUP_BONUS,
        }

        spending_types = {
            TransactionType.CONTENT_UNLOCKED,
        }

        if transaction_type in earning_types and amount < 0:
            raise ValueError(f"Transaction type {transaction_type} must have a positive amount ")
        elif transaction_type in spending_types and amount > 0:
            raise ValueError(f"Transaction amount exceeds maximum allowed (100,000 tokens)")
        
        if abs(amount) > 100000:
            raise ValueError("Transaction amounte exceeds max: 100,000 tokens")
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
                raise ValueError("Unlocked item ID required for CONTENT_UNLOCKED")
            if self.review_id:
                raise ValueError("Review ID should not be set for CONTENT_UNLOCKED")  
                
        elif self.transaction_type == TransactionType.SIGNUP_BONUS:
            if self.review_id or self.unlocked_item_id:
                raise ValueError(f"Transaction type {self.transaction_type} should not reference other entities") 
        
        return self
        
    @field_validator('idempotency_key')
    @classmethod
    def validate_idempotency_key(cls, key: Optional[str]) -> Optional[str]:
        if key is None:
            return None
        if not re.fullmatch(r'^[A-Za-z0-9_\-]+$', key):
            raise ValueError("Idempotency key must be URL safe (alphanumeric, _ or - only )")

        return key
    
class TokenTransactionResponse(TokenTransactionBase):
    id: int
    user_id: int 
    balance_after: int
    created_at: datetime

    review_id: Optional[int] = None
    unlocked_item_id: Optional[int] = None 

    display_description: Optional[str] = None
    is_credit: bool = Field(default=False)

    @model_validator(mode='after')
    def compute_display_fields(self) -> 'TokenTransactionResponse': 
        self.is_credit = self.amount > 0
        
        descriptions = {
            TransactionType.REVIEW_POSTED: f"Earned {abs(self.amount)} tokens for posting a review",
            TransactionType.SIGNUP_BONUS: f"Welcome bonus: {abs(self.amount)} tokens",
            TransactionType.CONTENT_UNLOCKED: f"Spent {abs(self.amount)} tokens to unlock content",
        }

        self.display_description = descriptions.get(
            self.transaction_type,
            f"{'Earned' if self.is_credit else 'Spent'} {abs(self.amount)} tokens"
        )

        return self
