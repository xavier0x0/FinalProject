from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import order_details as controller
from ..schemas import order_details as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Users'],
    prefix="/users"
)


@router.post("/", response_model=schema.OrderDetail)
def create(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)