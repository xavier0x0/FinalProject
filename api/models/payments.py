from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    payment_method = Column(String(50), nullable=False)
    card_number = Column(String(16), nullable=False)
    card_type = Column(String(20), nullable=False)
    expiration_date = Column(String(7), nullable=False)
    billing_address = Column(String(300), nullable=False)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="payments")