from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    payment_method: str = Field(..., max_length=60)
    card_type: Optional[str] = Field(None, max_length=20)
    card_number: Optional[str] = Field(None, min_length=16, max_length=16)
    expiration_date: Optional[str] = Field(None, regex=r"^(0[1-9]|1[0-2])\/\d{2}$")
    billing_address: Optional[str] = Field(None, max_length=400)
    amount: float = Field(..., gt=0)
    payment_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
