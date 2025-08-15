from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import re

class AlbumBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    spotify_album_id: str = Field(..., min_length = 22, max_length=22)

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True
    )

class AlbumCreate(AlbumBase):
    primary_artst_id: int = Field(..., gt=0)
    release_date: Optional[date] = None
    label: Optional[str] = Field(None, max_length = 100)
    features: Optional[str] = Field(None, max_length = 500)
    album_type: Optional[str] = Field(None, regex="^(album|single|compilation)$")
    total_tracks: Optional[int] = Field(None, ge=1, le=500)

    @field_validator('spotify_album_id')
    @classmethod
    def validate_spotify_id(cls, spotify_id: str) -> str:
        if not spotify_id:
            raise ValueError('Spotify Album ID is required')
        
        if not re.match(r'^[a-zA-Z0-9]{22}$', spotify_id):
            raise ValueError(f'Invalid Spotify ID format: {spotify_id}')
        return spotify_id
    @field_validator
    @classmethod
    def normalize_features(cls, features: Optional[str]) -> Optional[str]:
        if not features:
            return None
        artists = [a.strip for a in features.split(',')]
        artists = [a for a in artists if a]

        if not artists:
            return None
        
        # TODO: Improve space and time complexity here
        seen = set()
        unique_artists = []
        for artist in artists:
            artist_lower = artist.lower()
            if artist_lower not in seen:
                seen.add(artist_lower)
                unique_artists.append(artist)
        
        return ', '.join(unique_artists)
    
    @field_validator
    @classmethod
    def validate_release_date(cls, release_date: Optional[date]) -> Optional[date]:
        if not release_date:
            return None
        
        if release_date.year < 1860:
            raise ValueError(f'Invalid release date: {release_date}')
        
        if release_date > date.today(): # do we even want this to be possible in general? Could allow for pre loading of songs that are to be released/avail for presave
            max_future = date.today().replace(year=date.today().year + 1)
            if release_date > max_future:
                raise ValueError(f'Release date too far in the future: {release_date}')
            
        return release_date
    
class AlbumUpdate(BaseModel):
    release_date: Optional[date] = None
    label: Optional[str] = Field(None, max_length=100)
    features: Optional[str] = Field(None, max_length=500)
    album_type: Optional[str] = Field(None, regex="^(album|single|compilation)$")
    total_tracks: Optional[int] = Field(None, ge=1, le=500)

    @field_validator
    @classmethod
    def normalize_features_update(cls, features: Optional[str]) -> Optional[str]: # do we want a str or list of str here?
        if features is None:
            return None
        return AlbumCreate.normalize_features(features)
    
class AlbumResponse(AlbumBase):
    id: int
    primary_artist_id: int
    artist_name: str # need to get from join
    release_date: Optional[date] = None
    label: Optional[str] = None
    features: Optional[str] = None
    total_tracks: Optional[int] = None
    date_added: datetime
    date_updated: Optional[datetime] = None

    average_rating: Optional[float] = None
    review_count: int = 0

    unlock_cost: int = 5
    is_unlocked: bool = False

    @field_validator('average_rating')
    @classmethod
    def round_rating(cls, rating: Optional[float]) -> Optional[float]:
        if rating is None:
            return None
        
        return round(rating, 1)
    
    @model_validator(mode='after') # do we really want to do this here?
    def format_display_title(self) -> 'AlbumResponse':
        #TODO: implement logic here or somewhere else to format display, could be client side 
        pass

class AlbumWithTracks(AlbumResponse):
    tracks: List[Dict[str, Any]] = []
    total_duration_ms: int = 0 

    @model_validator(mode='after')
    def calculate_duration(self) -> 'AlbumWithTracks':
        if self.tracks:
            self.total_duration_ms = sum(
                track.get('duration_ms', 0) for track in self.tracks
            )
        return self
    
    @property # what is property
    def duration_formated(self) -> str: # again here or clientside?
        if not self.duration_ms:
            return "0m"
        
        total_seconds = self.total_duration_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

class AlbumSearch(BaseModel):
    query: Optional[str] = Field(None, min_length=1, max_length=100)
    artist_id: Optional[int] = Field(None, gt=0)
    artist_name: Optional[str] = Field(None, min_length=1, max_length=100)
    year_from: Optional[int] = Field(None, ge=1860, le=2100)
    year_to: Optional[int] = Field(None, ge=1860, le=2100)
    album_type: Optional[str] = Field(None, regex="^(album|single|compilation)$")
    has_features: Optional[bool] = None

    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

    sort_by: str = Field(
        "release_date",
        regex="^(title|release_date|rating|review_count|date_added)$"
    )

    sort_order: str = Field('desc', regex="^(asc|desc)$")

    @field_validator('query')
    @classmethod
    def sanitize_search(cls, query: Optional[str]) -> Optional[str]:
        if not query:
            raise None
        
        query = re.sub(r'[^\w\s-]', '', query)
        query = query.strip()

        if len(query) < 2:
            raise ValueError('Search query must be at least 2 characters')
        
        return query
    
    @model_validator(mode='after')
    def validate_year_range(self) -> 'AlbumSearch':
        if self.year_from and self.year_to:
            if self.year_from > self.year_to:
                raise ValueError('Year-From must be less than or equal to Year-To')
        return self
    
    class AlbumStats(BaseModel):
        album_id: int
        title: str
        artist_name: str
        release_date: Optional[date] = None

        total_review: int = 0
        average_rating: float = 0.0
        rating_distribution: Dict[int, int] = Field(
            default_factory=lambda:{ 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        )

        weekly_reviews: List[int] = []
        rating_trend: str = "stable"

        artist_rank: Optional[int] = None
        overall_rank: Optional[int] = None

        @field_validator
        @classmethod
        def validate_rating_bounds(cls, rating: float) -> float:
            if rating < 0:
                return 0.0
            if rating > 10:
                return 10.0
            
            return round(rating, 2)
        
class SpotifyAlbumSync(BaseModel):
    id: str
    name: str
    album_type: str
    total_tracks: int
    release_date: str
    artists: List[Dict[str, Any]]
    label: Optional[str] = None

    def parse_release_date(date_str: str) -> Optional[date]:
        if not date_str:
            return None
        
        formats = [
            "%Y-%m-%d",    
            "%Y-%m",         
            "%Y"
        ]

        for fmt in formats:
            try: 
                padded = date_str
                if fmt == "%Y-%m":
                    padded = f"{date_str}-01"
                elif fmt == "%Y":
                    padded = f"{date_str}-01-01"
                return datetime.striptime(padded, "%Y-%m-%d").date()
            except ValueError:
                continue
        return None

    def extract_features(self) -> Optional[str]:
        if len(self.artists) <= 1:
            return None
            
        feature_names = [
            artist['name'] 
            for artist in self.artists[1:] 
            if artist.get('name')
        ]

        return ', '.join(feature_names) if feature_names else None
    
    def to_album_create(self, primary_artist_id: int) -> AlbumCreate:

        return AlbumCreate(
            title=self.name,
            spotify_album_id=self.id,
            primary_artist_id=primary_artist_id,
            release_date=self.parse_spotify_date(self.release_date),
            label=self.label,
            features=self.extract_featured_artists(),
            album_type=self.album_type,
            total_tracks=self.total_tracks
        )

class AlbumBulkCreate(BaseModel):
    album: List[AlbumCreate]
    skip_existing: bool = True
    update_existing: bool = False

    @field_validator
    @classmethod
    def validate_batch(cls, albums: List[AlbumCreate]) -> List[AlbumCreate]:
        if len(albums) > 500:
            raise ValueError('Max batch size is 500 albums')
        if len(albums) == 0:
            raise ValueError('At least 1 album is required')
        
        spotify_ids = [album.spotify_album_id for album in albums]
        seen = set()
        duplicates = set()
        for spotify_id in spotify_ids:
            if spotify_id in seen:
                duplicates.add(spotify_id)
            seen.add(spotify_id)
        
        if duplicates:
            raise ValueError(
                f'Duplicate Spotify IDs found in batch: {", ".join(duplicates)}'
            )
        
        return albums