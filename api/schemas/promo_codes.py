from pydantic import BaseModel
from datetime import datetime

class PromoCodeBase(BaseModel):
    code: str
    discount_value: float
    is_percentage: bool
    expiration_date: datetime

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCode(PromoCodeBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
