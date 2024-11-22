from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="First Last")
    email: EmailStr = Field(..., example="example@example.com")


class CustomerCreate(CustomerBase):
    password: str = Field(..., min_length=6, max_length=100)


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True