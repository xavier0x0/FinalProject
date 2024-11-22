from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    price: int
    description: str
