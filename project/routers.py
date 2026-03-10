
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from models import (
    Order,
    User
)
from database import (
    engine
)
from users import (
    get_current_user
)

router = APIRouter()


@router.get("/MCDONALDS", tags=["Welcome"])
async def basic_welcome_to_everyone():
    return {"Message": "Welcome to McDonald's Order system."}


@router.post("/order", tags=["Items"])
async def create_order(order: Order, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
    return {
        "Message": "Order added successfully",
        "Order_id": f"#{order.id:03d}",
        "order": order
    }


@router.get("/orders", tags=["Items"])
async def kitchen_display():
    # We opening connect database same than create_order part.
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        return results.all()


@router.delete("/order/{order_id}", tags=["Items"])
async def delete_Orders(order_id: str, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        session.delete(order)
        session.commit()
        return {"Message": "Item deleted successfully"}


@router.put("/order/{order_id}/status",  tags=["Items"])
async def update_status(order_id: str, new_status: str, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = new_status
        session.commit()
        session.refresh(order)
        return order


@router.get("/order/completed",  tags=["Items"])
async def order_completed():
    with Session(engine) as session:
        statement = select(Order).where(Order.status == "Completed")
        results = session.exec(statement)
        return results.all()


@router.get("/order/pending",  tags=["Items"])
async def order_pending():
    with Session(engine) as session:
        statement = select(Order).where(Order.status == "Pending")
        results = session.exec(statement)
        return results.all()


@router.get("/order/total", tags=["Items"])
async def order_total():
    total = 0
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        orders = results.all()
        for order in orders:
            total = total + order.price
            return {"Total_price": total, "order_count": len(orders)}


@router.get("/order/{order_id}",  tags=["Items"])
async def one_order(order_id: str):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return order
