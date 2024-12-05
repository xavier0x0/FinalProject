from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import reviews as models
from ..schemas import reviews as schema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import literal

def create_review(db: Session, request: schema.ReviewCreate):
    review = models.Review(
        menu_item_id=request.menu_item_id,
        review_text=request.review_text,
        rating=request.rating
    )
    try:
        db.add(review)
        db.commit()
        db.refresh(review)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review

def get_all_reviews(db: Session):
    try:
        return db.query(models.Review).all()
    except SQLAlchemyError as e:
        error = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def get_reviews_by_menu_item(db: Session, menu_item_id: int):
    try:
        reviews = db.query(models.Review).filter(models.Review.menu_item_id == literal(menu_item_id)).all()
        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No reviews found for this menu item"
            )
        return reviews
    except SQLAlchemyError as e:
        error = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )
