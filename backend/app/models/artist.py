from sqlalchemy import Column, Integer, DateTime, String, CheckConstraint, NUMERIC, func
from sqlalchemy.orm import relationship
from app.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    artist_name = Column(String(100), unique=True, index=True, nullable=False)
    spotify_artist_id = Column(String(50), unique=True, index=True, nullable=False)
    popularity = Column(Integer)
    followers = Column(Integer)

    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    total_reviews = Column(Integer, default=0)
    average_rating = Column(NUMERIC(precision=3, scale=1), nullable=True)

    albums = relationship("Album", back_populates="primary_artist")
    songs = relationship("Song", back_populates="artist")
    reviews = relationship("Review", back_populates="artist", cascade="all, delete-orphan")
    unlocked_items = relationship("UnlockedItem", back_populates="artist", cascade="all, delete-orphan")


    __table_args__ = (
        CheckConstraint('popularity >= 0 AND popularity <= 100', name="check_popularity_range"),
        CheckConstraint('followers >= 0', name='check_followers_positive'),
    )

