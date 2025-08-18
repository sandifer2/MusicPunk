from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, CheckConstraint, Index, NUMERIC, func
from sqlalchemy.orm import relationship
from app.database import Base


class Song(Base):
    __tablename__= "songs"

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False, index=True)
    release_date = Column(Date, nullable=True, index=True)

    popularity = Column(Integer)
    features = Column(String(500))
    duration_ms = Column(Integer)

    total_reviews = Column(Integer, default=0)
    average_rating = Column(NUMERIC(precision=3, scale=1), nullable=True)

    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())

    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    reviews = relationship("Review", back_populates="song", cascade="all, delete-orphan")
    unlocked_items = relationship("UnlockedItem", back_populates="song", cascade="all, delete-orphan")


    __table_args__ = (
        CheckConstraint('popularity >= 0 AND popularity <= 100', name='check_song_popularity_range'),
        CheckConstraint('duration_ms > 0', name='check_duration_positive'),
        Index('idx_song_artist_album', 'artist_id', 'album_id'),
        Index('idx_song_popularity', 'popularity'),  
    )


