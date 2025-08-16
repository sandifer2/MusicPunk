from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, NUMERIC, Index, UniqueConstraint, CheckConstraint, Enum, func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class ReviewType(enum.Enum):
    SONG = "song"
    ALBUM = "album"
    ARTIST = "artist"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    song_id = Column(Integer, ForeignKey("songs.id", ondelete="CASCADE"), nullable=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=True)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=True)

    rating = Column(NUMERIC(precision=3, scale=1), nullable=False)
    review_text = Column(String(1000))

    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reviews")
    song = relationship("Song", back_populates="reviews")
    artist = relationship("Artist", back_populates="reviews")
    album = relationship("Album", back_populates="reviews")

    __table_args__ = (
        #converts bool to int (1 or 0) to ensure exactly 1 of the target ids are set
        CheckConstraint(
            "(song_id IS NOT NULL)::int + (album_id IS NOT NULL)::int + (artist_id IS NOT NULL)::int = 1", 
            name="check_exactly_one_item"
        ),
        UniqueConstraint('user_id', 'song_id', name='unique_user_song_review'),
        UniqueConstraint('user_id', 'album_id', name='unique_user_album_review'),
        UniqueConstraint('user_id', 'artist_id', name='unique_user_artist_review'),

        Index('idx_review_song', 'song_id'),
        Index('idx_review_album', 'album_id'),
        Index('idx_review_artist', 'artist_id'),
        Index('idx_review_user_date', 'user_id', 'date_added'),
        Index('idx_review_rating', 'rating'),
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_rating_range'),
        Index('idx_review_song_rating', 'song_id', 'rating'),  # avg rating per song
        Index('idx_review_album_rating', 'album_id', 'rating'),
        Index('idx_review_artist_rating', 'artist_id', 'rating'),
    )
