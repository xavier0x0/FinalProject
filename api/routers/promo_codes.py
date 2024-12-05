from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promo_codes as controller
from ..schemas import promo_codes as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promo Codes"],
    prefix="/promocodes",
)

# specfic format for dates: 2024-12-03T12:00:00
@router.post("/", response_model=schema.PromoCode)
def create_promo_code(request: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create_promo_code(db=db, request=request)

@router.delete("/{promo_id}")
def delete_promo_code(promo_id: int, db: Session = Depends(get_db)):
    controller.delete_promo_code(db, promo_id)
    return {"detail": "Promo code deleted successfully"}

@router.post("/apply", response_model=float)
def apply_promo_code(code: str, total_amount: float, db: Session = Depends(get_db)):
    return controller.apply_promo_code(db, code, total_amount)

@router.get("/", response_model=list[schema.PromoCode])
def list_promo_codes(db: Session = Depends(get_db)):
    return controller.list_promo_codes(db)
