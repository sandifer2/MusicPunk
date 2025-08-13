from pydantic import BaseModel, field_validator, model_validator
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
    def validate_rating(cls, rating):
        if rating is None:
            raise ValueError('Rating required. No rating found')
        if rating < 0 or rating > 10:
            raise ValueError('Rating must be between 0 and 10')
        return round(rating, 1)
    
    @field_validator('review_text')
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
    def validate_item_id(cls, id):
        if id <= 0:
            raise ValueError('Item ID must be a positive integer')
        return id
    
class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    reviewer_username: str
    date_added: datetime
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReviewDetails(ReviewResponse):
    item_title: str # TODO: query must be parameterized to match enum type of review 
    item_subtitle: Optional[str] = None #TODO: add logic so it returns only the artist attached to song when item is song or album, else none

    @model_validator(mode='after')
    def set_item_subtitle(self):
        if self.item_type == ReviewType.SONG:
            pass
        elif self.item_type == ReviewType.ALBUM:
            pass
        else:
            self.item_subtitle = None
        return self
    
class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    review_text: Optional[str] = None

    @field_validator('rating')
    def validate_rating(cls, rating):
        if rating is not None:
            if rating < 0 or rating > 10:
                raise ValueError('Rating must be between 0 and 10')
            return round(rating, 1)
        return rating
    
    @field_validator('review_text')
    def validate_review_text(cls, text):
        if text is None: return None
        
        text = text.strip()

        if len(text) == 0: return None

        if len(text) > 1000:
            raise ValueError('Review text exceeds max of 1000 characters')
        if len(text) < 5:
            raise ValueError('Review text must be longer than 5 characters if text is provided')
        
        return text
    
class ReviewStats(BaseModel):
    total_reviews: int
    average_rating: Optional[float] = None
    rating_distribution: dict = {}

    @field_validator('average_rating')
    def validate_average_rating(cls, rating):
        if rating is not None:
            if rating < 0 or rating > 10:
                raise ValueError('Average rating must be between 0 and 10')
            return round(rating, 1)
        return rating

        
        
    