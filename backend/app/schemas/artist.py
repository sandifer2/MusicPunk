from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from core.config import settings
import re

class ArtistBase(BaseModel):
    artist_name: str = Field(..., min_length=1, max_length=100)
    spotify_artist_id: str = Field(..., min_length=22, max_length=22)

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True
        
    )

class ArtistCreate(ArtistBase):
    popularity: Optional[int] = Field(None, ge=0, le=100) 
    followers: Optional[int] = Field(None, ge=0)
    genres: Optional[List[str]] = []

    @field_validator('spotify_artist_id')
    @classmethod
    def validate_spotify_id(cls, spotify_id:str) -> str:
        if not spotify_id:
            raise ValueError('Spotify artist ID is required')
        
        if not re.match(r'^[a-zA-Z0-9]{22}$', spotify_id):
            raise ValueError (f'Invalid Spotify ID format. Expected 22 base-62 characters, got {spotify_id}')
        
        return spotify_id
    
    @field_validator('genres')
    @classmethod
    def normalize_generes(cls, genres: Optional[List[str]]) -> List[str]:
        if not genres:
            return []
        
        normalized = []
        for genre in genres:
            clean=genre.lower().strip()
            clean = clean.replace('&', 'and')
            clean = clean.replace('-', ' ')
            clean = ' '.join(clean.split())

            if clean and clean not in normalized:
                normalized.append(clean)
        return normalized
    

    
class ArtistResponse(ArtistBase):
    id: int
    popularity: Optional[int] = None
    followers: Optional[int] = None
    date_added: datetime
    date_updated: Optional[datetime] = None

    album_count: int = 0
    song_count: int = 0
    average_rating: Optional[float] = None
    review_count: int = 0

    unlock_cost: int = Field(default_factory=lambda: settings.TOKENS_UNLOCK_COST)
    is_unlocked: bool = False

    @field_validator('average_rating')
    @classmethod
    def round_rating(cls, rating: Optional[float]) -> Optional[float]:
        if rating is None:
            return None
        return round(rating, 1)
    




