from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Tuple
from datetime import datetime 
from enum import Enum
import re
from core.config import settings

class ReviewType(str, Enum):
    SONG = 'SONG'
    ALBUM = 'ALBUM'
    ARTIST = 'ARTIST'


class UnlockedItemBase(BaseModel):
    item_type: ReviewType
    item_id: int = Field(..., gt=0)

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True        
    )


class UnlockedItemCreate(UnlockedItemBase):
    user_id: int = Field(..., gt=0)

    @field_validator('item_id')
    @classmethod
    def validate_item_id(cls, id: int) -> int:
        if id <= 0:
            raise ValueError('item_id must be a positive integer')
        return id
    
class UnlockRequest(UnlockedItemBase): # way over my head need deep explaination on this 

    idempotency_key: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=64,
        description="Client-generated key to make unlock attempts idempotent"
    )

    @field_validator('idempotency_key')
    @classmethod
    def validate_idempotency_key(cls, key: Optional[str]) -> Optional[str]:
        if key is None:
            return None
        if not re.match(r'^[A-Za-z0-9_\-]+$', key):
            raise ValueError('Idempotency key must be URL safe: (A-Za-z0-9_- only)')
        return key
    
class UnlockResult(BaseModel):
    success: bool
    already_unlocked: bool = False
    tokens_charged: int = 0
    remaining_tokens: int = 0 
    message: str

class UnlockedItemResponse(UnlockedItemBase):
    item_type: ReviewType
    item_id: int
    item_name: str
    is_unlocked: bool = False
    has_reviewed: bool = False
    unlock_cost: int = Field(default_factory=lambda: settings.TOKENS_UNLOCK_COST)
    user_tokens: Optional[int] = None
    unlocked_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


