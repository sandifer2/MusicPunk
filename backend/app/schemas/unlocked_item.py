from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Tuple
from datetime import datetime 
from enum import Enum
import re

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

    @field_validator
    @classmethod
    def validate_item_id(cls, id: int) -> int:
        if id <= 0:
            raise ValueError('item_id must be a positive integer')
        return id
    
class UnlockRequest(UnlockedItemBase): # way over my head need deep explaination on this 

    expected_cost: int = Field(5, ge=1, le=10_000)
    idempotency_key: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=64,
        description="Client supplied key to make unlock attempts idempotent"
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
    successL: bool
    already_unlocked: bool = False
    charged_tokens: int = 0
    remaining_tokens: Optional[int] = None
    unlocked_at: Optional[datetime] = None
    message: Optional[str] = None

class UnlockedItemResponse(UnlockedItemBase):
    id: int
    user_id: int
    is_unlocked: bool = False
    has_reviewed: bool = False
    unlock_cost: int = 10
    user_tokens: Optional[int] = None

class UnlockedItemSearch(BaseModel):
    user_id: Optional[int] = Field(None, gt=0)
    item_type: Optional[ReviewType] = None
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

    @model_validator(mode='after')
    def require_filter_for_admin_scale(self) -> 'UnlockedItemSearch': #what in gods name 
        #enforce something in routes instead
        return self 

