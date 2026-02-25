
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
order_list = []


class Order(BaseModel):
    id: str | None = None
    item: str
    status: str = "Pending"
    price: float


@app.get("/")
async def basic_welcome_to_everyone():
    return {"Message": "Welcome to McDonald's Order system."}


@app.post("/order")
async def create_order(order: Order):
    order = order.model_copy(update={"id": f"#{len(order_list) + 1:03d}"})
    order_list.append(order)
    return {"Message": "order added successfully", "order": order}


@app.get("/orders")
async def kitchen_display():
    return order_list


@app.delete("/order/{order_id}")
async def delete_Orders(order_id: str):
    for order in order_list:
        if order.id == order_id:
            order_list.remove(order)
            return {"Message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")


@app.put("/order/{order_id}/status")
async def status(order_id: str, new_status: str):
    for order in order_list:
        if order.id == order_id:
            order.status = new_status
            return {"Message": "Item completed"}
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/order/completed")
async def order_completed():
    completed_orders = []
    for order in order_list:
        if order.status == "Completed":
            completed_orders.append(order)
    return completed_orders


@app.get("/order/pending")
async def order_pending():
    pending = []
    for order in order_list:
        if order.status == "pending":
            pending.append(order)
        return pending


@app.get("/Welcome")
async def welcome_back():
    return {"Message": "Thank you for visiting, and welcome back."}
