from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class ReviewType(str, Enum):
    SONG = 'SONG'
    ALBUM = 'ALBUM'
    ARTIST = 'ARTIST'

class ReviewBase(BaseModel):
    item_type: ReviewType
    item_id: int
    rating: float
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    
    @field_validator('rating')
    @classmethod
    def validate_rating(cls, rating):
        if rating is None:
            raise ValueError('Rating required. No rating found')
        if rating < 0 or rating > 10:
            raise ValueError('Rating must be between 0 and 10')
        return round(rating, 1)
    
    @field_validator('review_text')
    @classmethod
    def validate_review_text(cls, text):
        if text is None: return None
        
        text = text.strip()

        if len(text) == 0: return None

        if len(text) > 1000:
            raise ValueError('Review text exceeds max of 1000 characters')
        if len(text) < 5:
            raise ValueError('Review text must be longer than 5 characters if text is provided')
        
        return text
    
    @field_validator('item_id')
    @classmethod
    def validate_item_id(cls, id):
        if id <= 0:
            raise ValueError('Item ID must be a positive integer')
        return id
    
class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    username: str
    date_added: datetime
    date_updated: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes = True
    )

class ReviewDetails(ReviewResponse):
    item_title: str #song/artist/album title
    item_subtitle: Optional[str] = None # artist for song/album


    
class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    review_text: Optional[str] = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, rating):
        if rating is not None:
            if rating < 0 or rating > 10:
                raise ValueError('Rating must be between 0 and 10')
            return round(rating, 1)
        return rating
    
    @field_validator('review_text')
    @classmethod
    def validate_review_text(cls, text):
        if text is None: return None
        
        text = text.strip()

        if len(text) == 0: return None

        if len(text) > 1000:
            raise ValueError('Review text exceeds max of 1000 characters')
        if len(text) < 5:
            raise ValueError('Review text must be longer than 5 characters if text is provided')
        
        return text
    


        
        
    