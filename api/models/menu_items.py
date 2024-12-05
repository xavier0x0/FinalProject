from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from .recipes import Recipe
from .resources import Resource

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    price = Column(Integer)
    calories = Column(Integer)
    name = Column(String(100))
    description = Column(String(300))
    category = Column(String(50), nullable=True)  # Added category field for filtering
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredients = Column(String(1000))
    reviews = relationship(relationship("Review"), back_populates="menu_item")
