from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Optional, List
from datetime import datetime 
from core.config import settings

class SongBase(BaseModel):
    title: str
    spotify_id: str
    popularity: Optional[int] = None
    features: Optional[str] = None

class SongCreate(SongBase):
    artist_id: int
    album_id: int

    @field_validator('title')
    @classmethod
    def validate_title(cls, title):
        if not title or not title.strip():
            raise ValueError('Song title cannot be empty')
        
        if len(title.strip()) > 200:
            raise ValueError('Song title exceeds 200 character maximum')
        return title.strip()

    @field_validator('spotify_id')
    @classmethod
    def validate_spotify_id(cls, id):
        if not id or len(id) != 22:
            raise ValueError('Invalid Spotify ID: empty ID or length not 22')
        return id

class SongReturn(SongBase):
    id: int
    artist_name: str
    album_name: str
    date_added: datetime
    date_updated: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes = True
    )

class SongUnlockStatus(SongReturn): 
    average_rating: Optional[float] = None
    review_count: int = 0
    is_unlocked: bool = False
    has_reviewed: bool = False
    unlock_cost: int = Field(default_factory=lambda: settings.TOKENS_UNLOCK_COST)

class SongSearchResults(BaseModel):
    id: int
    title: str
    artist_name: str
    album_name: str
    spotify_id: str
    review_count: int = 0
    average_rating: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True
    )




