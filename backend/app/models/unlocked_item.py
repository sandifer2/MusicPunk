from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, UniqueConstraint, func
from app.database import Base
from app.models.review import ReviewType


class UnlockedItem(Base):
    __tablename__ = "unlocked_items"

    id= Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_type = Column(Enum(ReviewType), nullable=False)
    item_id = Column(Integer, nullable=False, index=True)
    unlocked_date = Column(DateTime(timezone=True), server_default=func.now())


    __table_args__ = (UniqueConstraint('user_id', 'item_type', 'item_id', name='unique_user_item'),)