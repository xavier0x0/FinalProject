from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    price: int
    description: str
    category: Optional[str] = None # Added for filtering

class MenuItemsCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
