from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from core.config import settings
import re

class AlbumBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    spotify_album_id: str = Field(..., min_length = 22, max_length=22)

    model_config = ConfigDict(
        from_attributes=True, # allow attributes from obj, rather than just dict()
        validate_assignment=True, #validate on initialization and assignment
        str_strip_whitespace=True, 
        use_enum_values=True #clean serialization when returning json
    )

class AlbumCreate(AlbumBase):
    primary_artist_id: int = Field(..., gt=0)
    release_date: Optional[date] = None
    label: Optional[str] = Field(None, max_length = 100)
    features: Optional[str] = Field(None, max_length = 500)
    album_type: Optional[str] = Field(None, regex="^(album|single|compilation)$") #TODO: change to enum types
    total_tracks: Optional[int] = Field(None, ge=1, le=500)

    @field_validator('spotify_album_id')
    @classmethod
    def validate_spotify_id(cls, spotify_id: str) -> str:
        if not spotify_id:
            raise ValueError('Spotify Album ID is required')
        
        if not re.fullmatch(r'^[a-zA-Z0-9]{22}$', spotify_id):
            raise ValueError(f'Invalid Spotify ID format: {spotify_id}')
        return spotify_id
    
    @field_validator('features')
    @classmethod
    def normalize_features(cls, features: Optional[str]) -> Optional[str]:
        if not features:
            return None
        artists = [a.strip() for a in features.split(',')]
        artists = [a for a in artists if a]

        if not artists:
            return None

        seen = set()
        unique_artists = []
        for artist in artists:
            artist_lower = artist.lower()
            if artist_lower not in seen:
                seen.add(artist_lower)
                unique_artists.append(artist)
        
        return ', '.join(unique_artists)
    
    @field_validator('release_date')
    @classmethod
    def validate_release_date(cls, release_date: Optional[date]) -> Optional[date]:
        if not release_date:
            return None
        if release_date.year < 1860:
            raise ValueError(f'Invalid release date: {release_date}')
            
        return release_date
    
class AlbumResponse(AlbumBase):
    id: int
    primary_artist_id: int
    artist_name: str # comes from hybrid property
    release_date: Optional[date] = None
    label: Optional[str] = None
    features: Optional[str] = None
    total_tracks: Optional[int] = None
    date_added: datetime
    date_updated: Optional[datetime] = None

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

class AlbumQuickSearch(BaseModel):
    '''Compact album for search/lists'''
    id: int
    title: str
    spotify_album_id: str
    artist_name: str
    release_date: Optional[date] = None
    average_rating: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True
    )