from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from datetime import datetime
from ..dependencies.database import Base

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)  # Unique promo code
    discount_value = Column(DECIMAL(10, 2), nullable=False)  # Flat discount
    is_percentage = Column(Boolean, default=False)  # True if discount is percentage
    expiration_date = Column(DATETIME, nullable=False)  # Expiration date
    is_active = Column(Boolean, default=True)  # Whether the code is active
