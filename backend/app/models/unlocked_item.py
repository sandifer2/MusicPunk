from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Index, Enum, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base





class UnlockedItem(Base):
    __tablename__ = "unlocked_items"

    id= Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    song_id = Column(Integer, ForeignKey("songs.id", ondelete="CASCADE"), nullable=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=True)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=True)



    unlocked_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tokens_spent = Column(Integer, nullable=False, default=5)

    user = relationship("User", back_populates="unlocked_items")
    song = relationship("Song", back_populates="unlocked_items")
    album = relationship("Album", back_populates="unlocked_items")
    artist = relationship("Artist", back_populates="unlocked_items")

    __table_args__ = (
       #converts bool to int (1 or 0) to ensure exactly 1 of the target ids are set
       CheckConstraint(
           "(song_id IS NOT NULL)::int + (album_id IS NOT NULL)::int + (artist_id IS NOT NULL)::int = 1",
           name="check_exactly_one_unlocked"
       ),

       UniqueConstraint('user_id', 'song_id', name='unique_user_song_unlock'),
       UniqueConstraint('user_id', 'album_id', name='unique_user_album_unlock'),
       UniqueConstraint('user_id', 'artist_id', name='unique_user_artist_unlock'),

       Index('idx_unlock_song', 'song_id'),
       Index('idx_unlock_album', 'album_id'),
       Index('idx_unlock_artist', 'artist_id'),
   )