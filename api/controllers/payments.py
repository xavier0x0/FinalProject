from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import payments as model
from ..models import orders as order_model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas import payments as schema
from datetime import datetime


def create(db: Session, request: schema.PaymentCreate):
    # Check if the order exists
    order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found!"
        )

    # Ensure the payment amount matches the order total price
    if request.amount != float(order.total_price):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount ({request.amount}) does not match the order total price ({order.total_price})."
        )

    # Create a new payment record
    new_payment = model.Payment(
        order_id=request.order_id,
        card_type=request.card_type,
        card_number=request.card_number,
        expiration_date=request.expiration_date,
        billing_address=request.billing_address,
        amount=request.amount,
        payment_status="Completed",  # Assume payment is completed for simplicity
        payment_date=datetime.utcnow(),
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Database error: {error}"
        )

    return new_payment
