from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False )
    primary_artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False, index=True)
    spotify_album_id = Column(String(100),unique=True, nullable=False, index=True)
    release_date = Column(DateTime)
    label = Column(String(50))
    features = Column(String(200), index=True)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())





