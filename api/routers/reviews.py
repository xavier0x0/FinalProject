from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews"
)

@router.post("/", response_model=schema.Review)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create_review(db=db, request=request)


@router.get("/", response_model=list[schema.Review])
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.get_all_reviews(db)

@router.get("/menu-item/{menu_item_id}", response_model=list[schema.Review])
def get_reviews_by_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.get_reviews_by_menu_item(db, menu_item_id)
