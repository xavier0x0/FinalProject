from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PromotionBase(BaseModel):
    description: Optional[str] = Field(None, max_length=300)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    discount: float = Field(..., gt=0, le=100)


class PromotionCreate(PromotionBase):
    menu_item_id: int = Field(...)


class PromotionUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=300)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    discount: Optional[float] = Field(None, gt=0, le=100)


class Promotion(PromotionBase):
    id: int
    menu_item_id: int

    class Config:
        orm_mode = True
