from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from ..models import resources as Resource, sandwiches as Sandwich
from ..schemas import order_details as schema
from datetime import datetime




def create(db: Session, request: schema.OrderDetailCreate):
    try:
        with db.begin():  # Ensures atomicity
            # Validate ingredient availability
            validate_ingredients(db=db, sandwich_id=request.sandwich_id, order_amount=request.amount)

            # Deduct ingredients
            sandwich = db.query(Sandwich).filter(Sandwich.id == request.sandwich_id).first()
            if not sandwich:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")

            for recipe_item in sandwich.recipes:
                resource = db.query(Resource).filter(Resource.id == recipe_item.resource_id).first()
                resource.amount -= recipe_item.amount * request.amount

            # Create the order
            new_order = model.Order(
                customer_name=request.customer_name,  # Optional
                description=f"{request.amount} x {sandwich.sandwich_name}",  # Order summary
                order_date=datetime.now(),  # Automatically set order date
                total_price=float(sandwich.price) * request.amount  # Calculate total price
            )
            db.add(new_order)

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order



def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def validate_ingredients(db: Session, sandwich_id: int, order_amount: int):
    # Fetch the sandwich details
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")

    # Validate each ingredient's availability
    for recipe_item in sandwich.recipes:
        resource = db.query(Resource).filter(Resource.id == recipe_item.resource_id).first()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ingredient {resource.item} not found!")

        if resource.amount < recipe_item.amount * order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient {resource.item} to fulfill the order!"
            )