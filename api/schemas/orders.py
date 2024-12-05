from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    total_price: Optional[float] = None
    order_type: str = Field(..., description="Order type, Takeout or Delivery") # Field for takeout/delivery preference
    order_date: datetime

    # Validator to ensure valid order types
    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v):
        allowed_types = ["Takeout", "Delivery"]
        if v not in allowed_types:
            raise ValueError(f"Invalid order type. Must be one of: {', '.join(allowed_types)}")
        return v

class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True

