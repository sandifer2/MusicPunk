from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,  func
from app.database import Base


class Song(Base):
    __tablename__= "songs"

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False, index=True)
    popularity = Column(Integer)
    features = Column(String(200),index=True)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())


