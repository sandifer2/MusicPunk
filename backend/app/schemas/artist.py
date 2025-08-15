from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
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
    popularity: Optional[int] = Field(None, ge=0, le=100) # what does ge and le mean and why are we adding Field and not just Optional[int] = None
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
    
class ArtistUpdate(BaseModel):

    popularity: Optional[int] = Field(None, ge=0, le=100)
    followers: Optional[int] = Field(None, ge=0)
    genres: Optional[List[str]] = None

    @field_validator('genres')
    @classmethod
    def normalize_genres_update(cls, genres: Optional[List[str]]) -> Optional[List[str]]:
        if genres is None:
            return None
        return ArtistCreate.normalize_generes(genres)
    
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

    unlock_cost: int = 5
    is_unlocked: bool = False

    @field_validator('average_rating')
    @classmethod
    def rount_rating(cls, rating = Optional[float]) -> Optional[float]:
        if rating is None:
            return None
        return round(rating, 1)
    
class ArtistStats(ArtistResponse):
    total_reviews: int = 0
    rating_distribution: Dict[int, int] = Field(
        default_factory=lambda: {1:0, 2:0, 3: 0, 4: 0, 5: 0} # what on earth is this doing
    )   
    recent_reviews: List[Dict[str, Any]] = []
    top_songs: List[Dict[str, Any]] = []
    top_albums: List[Dict[str, Any]] = []

    popularity_trend: str = "stable" # rising, falling, stable
    monthly_review_growth: float = 0.0

    @model_validator(mode='after')
    def calulate_trend(self) -> 'ArtistStats':
        '''
        Last 30 days vs prev 30 days
        '''
        pass

class ArtistSearch(BaseModel):
    query: Optional[str] = Field(None, min_length=1, max_length=100)
    genres: Optional[List[str]] = None
    min_pop: Optional[int] = Field(None, ge=0, le=100)
    min_followers: Optional[int] = Field(None, ge=0)

    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

    sort_by: str = Field("popularity", regex="^(name|popularity|followers|date_added)$")
    sort_order: str = Field("desc", regex="^(asc|desc)$")

    @field_validator('query')
    @classmethod
    def sanitize_query(cls, query: Optional[str]) -> Optional[str]:
        if not query:
            return None
        
        query = re.sub(r'[^\w\s-]', '', query)
        query = query.strip()

        if len(query) < 2:
            raise ValueError('Search Query must be at least 2 characters')

        return query
    
    @model_validator
    def validate_pagnation(self) -> 'ArtistSearch': # what is pagination 
        if self.offset + self.limit > 10000:
            raise ValueError('Deep pagination not allowed. Use cursor-based pagination for large datasets')
        return self
    
class ArtistBulkCreate(BaseModel):

    artists: List[ArtistCreate]
    skip_existing: bool = True
    update_existing: bool = False

    @field_validator('artists')
    @classmethod 
    def validate_batch_size(cls, artists: List[ArtistCreate]) -> List[ArtistCreate]:
        if len(artists) > 1000:
            raise ValueError('Too many artist in batch. Max: 1000')
        
        if len(artists) == 0:
            raise ValueError('No artists found')
        
        spotify_ids = [a.spotify_artist_id for a in artists]
        if len(spotify_ids) != len(set(spotify_ids)):
            raise ValueError('Duplicate IDs found in batch')
        
        return artists
    
    @model_validator
    def validate_flags(self) -> 'ArtistBulkCreate':
        if self.skip_existing and self.update_existing:
            raise ValueError('Cannot both skip and update existing records')
        return self
    
class SpotifyArtistSync(BaseModel):
    id: str 
    name: str
    popularity: int
    followers: Dict[str, Any]
    genres: List[str]
    images: List[Dict[str, Any]]

    def to_artist_create(self) -> ArtistCreate:
        return ArtistCreate(
            artist_name= self.name,
            spotify_artist_id= self.id,
            popularity= self.popularity,
            followers= self.followers.get('total', 0),
            genres= self.genres
        )
