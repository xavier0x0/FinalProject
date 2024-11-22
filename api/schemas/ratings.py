from pydantic import BaseModel, Field
from typing import Optional

class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(None, max_length=300)

class RatingCreate(RatingBase):
    menu_item_id: int = Field(...)

class Rating(RatingBase):
    id: int
    menu_item_id: int

    class Config:
        orm_mode = True