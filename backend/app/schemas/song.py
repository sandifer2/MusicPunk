from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime 

class SongBase(BaseModel):
    title: str
    spotify_id: str
    popularity: Optional[int] = None
    features: Optional[str] = None

class SongCreate(SongBase):
    artist_id: int
    album_id: int

    @field_validator('title')
    def validate_title(cls, title):
        if not title or not title.strip():
            raise ValueError('Song title cannot be empty')
        
        if len(title.strip()) > 200:
            raise ValueError('Song title exceeds 200 character maximum')
        return title.strip()

    @field_validator('spotify_id')
    def validate_spotify_id(cls, id):
        if not id or len(id) != 22:
            raise ValueError('Invalid Spotify ID: empty ID or length not 22')
        return id

class SongReturn(SongBase):
    id: int
    artist_name: str
    album_name: str
    date_added: datetime
    date_updated: datetime[Optional] = None

    model_config = ConfigDict(
        from_attributes = True
    )

class SongUnlockStatus(SongReturn): #has forward references to logic TODO in Reviews 
    average_rating: Optional[float] = None
    review_count: int = 0
    is_unlocked: bool = False
    has_reviewed: bool = False
    unlock_cost: int = 5
    
    
    @field_validator('average_rating') #TODO: create logic for average rating
    def validate_rating(cls, rating):

        if rating is None: return None

        if rating < 0 or rating > 10:
            raise ValueError('Average rating must be between 0 and 10')
        return round(rating, 1) 
    
class SongReviews(SongUnlockStatus): 
    reviews: List['ReviewResponse'] = [] #TODO implement review response in review schema

class SongUnlockReviews(BaseModel):
    song_id: str

    @field_validator('song_id')
    def validate_song_id(cls, id):
        if not id:
            raise ValueError('Song ID is required and not found')
        return id

class SongSearchResults(BaseModel):
    id: int
    title: str
    artist_name: str
    album_name: str
    spotify_id: str
    review_count: int = 0




