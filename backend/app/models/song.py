from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base


class Song(Base):
    __tablename__= "songs"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, index=True)
    artist_name = Column(String(200), nullable=False, index=True)
    album_name = Column(String(200), nullable=False)
    duration_ms = Column(Integer)
    popularity = Column(Integer)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
