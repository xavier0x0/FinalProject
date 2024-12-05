from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..models import promo_codes as models
from ..schemas import promo_codes as schema
from sqlalchemy.sql.expression import literal


# Create a new promo code
def create_promo_code(db: Session, request: schema.PromoCodeCreate):
    promo = models.PromoCode(
        code=request.code,
        discount_value=request.discount_value,
        is_percentage=request.is_percentage,
        expiration_date=request.expiration_date,
        is_active=True  # Default to active
    )
    try:
        db.add(promo)
        db.commit()
        db.refresh(promo)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )
    return promo

# Delete a promo code
def delete_promo_code(db: Session, promo_id: int):
    promo = db.query(models.PromoCode).filter(models.PromoCode.id == literal(promo_id)).first()
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promo code not found"
        )
    try:
        db.delete(promo)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )

# Validate and apply a promo code
def apply_promo_code(db: Session, code: str, total_amount: float):
    promo = db.query(models.PromoCode).filter(
        models.PromoCode.code == literal(code),
        models.PromoCode.is_active == literal(True)
    ).first()
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or inactive promo code"
        )
    if promo.expiration_date < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Promo code has expired"
        )
    # Calculate the discount
    discount = promo.discount_value if not promo.is_percentage else total_amount * (promo.discount_value / 100)
    return max(0, total_amount - discount)  # Ensure the total doesn't go below 0

def list_promo_codes(db: Session):
    try:
        return db.query(models.PromoCode).all()
    except SQLAlchemyError as e:
        error = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )
