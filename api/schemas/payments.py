from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class PaymentBase(BaseModel):
    card_type: str = Field(..., max_length=20)  # e.g., Visa, MasterCard
    card_number: str = Field(..., min_length=16, max_length=16)  # Must be exactly 16 digits
    expiration_date: str = Field(..., regex=r"^(0[1-9]|1[0-2])\/\d{2}$")  # MM/YY format
    billing_address: str = Field(..., max_length=400)
    amount: float = Field(..., gt=0)  # Must be greater than 0
    payment_date: Optional[datetime] = Field(default_factory=datetime.current)  # Default to current time

    # Custom validator to ensure card_number is numeric
    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, v):
        if not v.isdigit():
            raise ValueError("Card number must contain only digits.")
        return v


class PaymentCreate(PaymentBase):
    order_id: int  # Link to a specific order


class Payment(PaymentBase):
    id: int
    payment_status: str  # e.g., "Pending", "Completed"

    class Config:
        from_attributes = True
