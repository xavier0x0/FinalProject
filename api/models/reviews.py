from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    review_text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)  # Rating out of 5
    created_at = Column(DATETIME, default=datetime.utcnow)

    menu_item = relationship("MenuItem", back_populates="reviews")
