from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum, NUMERIC, func
import enum
from app.database import Base

class ReviewType(enum.Enum):
    SONG = "song"
    ALBUM = "album"
    ARTIST = "artist"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_type = Column(Enum(ReviewType), nullable=False)
    item_id = Column(Integer, nullable=False, index=True)
    rating = Column(NUMERIC(precision=3, scale=1), nullable=False)
    review_text = Column(String(1000))
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
