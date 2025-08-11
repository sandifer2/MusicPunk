from sqlalchemy import Column, Integer, DateTime, String, func
from app.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    artist_name = Column(String(100), unique=True, index=True, nullable=False)
    spotify_artist_id = Column(String(100), unique=True, index=True, nullable=False)
    popularity = Column(Integer)
    followers = Column(Integer)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

