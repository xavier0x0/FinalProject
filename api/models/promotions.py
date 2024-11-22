from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    menu_item = relationship("MenuItem", back_populates="promotions")
    description = Column(String(300))
    start_date = Column(DATETIME)
    end_date = Column(DATETIME)
    discount = Column(DECIMAL(5,2))