from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from datetime import date
from datetime import datetime

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.get("/status/{tracking_number}")
def track_order_status(tracking_number: int, db: Session = Depends(get_db)):
    """
    Track the status of an order by its tracking number.
    """
    return controller.get_status_by_tracking_number(db=db, tracking_number=tracking_number)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/revenue", response_model=dict)
def get_revenue_by_date(date: date, db: Session = Depends(get_db)):
    return controller.calculate_revenue_by_date(db=db, date=date)

@router.get("/date-range", response_model=list[schema.Order])
def get_orders_by_date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    return controller.get_orders_by_date_range(db=db, start_date=start_date, end_date=end_date)