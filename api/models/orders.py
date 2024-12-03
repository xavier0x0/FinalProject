from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=True) # Optional for anoymous customers
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) # Optional
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300), nullable=True) # Optional
    tracking_number = Column(Integer, nullable=True) # Optional
    status = Column(String(10), nullable=True, server_default="Pending") # Default to "Pending"
    total_price = Column(DECIMAL(5,2), nullable=True)
    order_type = Column(String(20), nullable=False) # Field for takeout/delivery

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)  # One-to-One relationship
