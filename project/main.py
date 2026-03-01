
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    status: str = "Pending"
    price: float


engine = create_engine("sqlite:///./project/mcd-order.db")
SQLModel.metadata.create_all(engine)


@app.get("/")
async def basic_welcome_to_everyone():
    return {"Message": "Welcome to McDonald's Order system."}


@app.post("/order")
async def create_order(order: Order):
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
    return {
        "Message": "Order added successfully",
        "Order_id": f"#{order.id:03d}",
        "order": order
    }


@app.get("/orders")
async def kitchen_display():
    # We opening connect database same than create_order part.
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        return results.all()


@app.delete("/order/{order_id}")
async def delete_Orders(order_id: str):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        session.delete(order)
        session.commit()
        return {"Message": "Item deleted successfully"}


@app.put("/order/{order_id}/status")
async def update_status(order_id: str, new_status: str):
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


@app.get("/order/completed")
async def order_completed():
    with Session(engine) as session:
        statement = select(Order).where(Order.status == "Completed")
        results = session.exec(statement)
        return results.all()


@app.get("/order/pending")
async def order_pending():
    with Session(engine) as session:
        statement = select(Order).where(Order.status == "Pending")
        results = session.exec(statement)
        return results.all()


@app.get("/order/total")
async def order_total():
    total = 0
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        orders = results.all()
        for order in orders:
            total = total + order.price
    return {"Total_price": total, "order_count": len(orders)}


@app.get("/order/{order_id}")
async def one_order(order_id: str):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return order


@app.get("/Welcome")
async def welcome_back():
    return {"Message": "Thank you for visiting, and welcome back."}
