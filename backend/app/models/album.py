from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, NUMERIC, func
from sqlalchemy.orm import relationship
from app.database import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False )
    primary_artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False, index=True)
    spotify_album_id = Column(String(50),unique=True, nullable=False, index=True)
    release_date = Column(Date)
    label = Column(String(100))
    features = Column(String(500))

    total_reviews = Column(Integer, default=0)
    average_rating = Column(NUMERIC(precision=3, scale=1), nullable=True)


    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    primary_artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="album", cascade="all, delete-orphan")
    unlocked_items = relationship("UnlockedItem", back_populates="album", cascade="all, delete-orphan")






