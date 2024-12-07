from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from ..models import resources as Resource, sandwiches as Sandwich
from ..schemas import orders as schema
from datetime import datetime
#error here? needed for calc revenue by  IDK what to set this as
from ..models import menu_items as models
from sqlalchemy.sql import func


def create(db: Session, request: schema.OrderCreate):
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

                # Ensure no negative inventory
                if resource.amount < 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient {resource.item} remaining in inventory!"
                    )

            # Create the order
            new_order = model.Order(
                customer_name=request.customer_name,  # Optional
                description=f"{request.amount} x {sandwich.sandwich_name}",  # Order summary
                total_price=float(sandwich.price) * request.amount,
                order_date=datetime.now(),  # Automatically set order date
                order_type=request.order_type, # Store order type
                status="Pending"
            )
            db.add(new_order)

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
            )

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
        
def get_status_by_tracking_number(db: Session, tracking_number: int):
    # Validate tracking number
    if tracking_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tracking number provided!"
        )
    
    try:
        # Query the order by tracking number
        order = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order with this tracking number not found!"
            )
        return {"tracking_number": tracking_number, "status": order.status}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )

def calculate_revenue_by_date(db: Session, date: datetime):
    try:
        # Query to calculate total revenue for the given day
        total_revenue = db.query(func.sum(models.OrderDetail.amount * models.MenuItem.price))\
                          .join(models.MenuItem, models.OrderDetail.sandwich_id == models.MenuItem.id)\
                          .join(models.Order, models.OrderDetail.order_id == models.Order.id)\
                          .filter(func.date(models.Order.order_date) == date.date())\
                          .scalar()

        return {"total_revenue": total_revenue or 0.0}  # Return 0 if no revenue found

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating revenue: {str(e)}")

def get_orders_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    try:
        # Query orders within the date range
        orders = db.query(models.Order).filter(
            models.Order.order_date >= start_date,
            models.Order.order_date <= end_date
        ).all()

        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")