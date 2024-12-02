from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Menu Items"],
    prefix="/menu_items"
)

@router.post("/", response_model=schema.MenuItemBase)
def create(request: schema.MenuItemBase, db: Session = Depends(get_db)):
    return controller.create_menu_item(db=db, request=request)

@router.get("/", response_model=list[schema.MenuItemBase])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all_menu_items(db)

@router.get("/{item_id}", response_model=schema.MenuItemBase)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_menu_item(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.MenuItemBase)
def update(item_id: int, request: schema.MenuItemBase, db: Session = Depends(get_db)):
    return controller.update_menu_item(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete_menu_item(db=db, item_id=item_id)
