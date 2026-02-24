
from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()
order_list = []


class Order(BaseModel):
    id: str | None = None
    item: str
    status: str = "Pending"


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
    return {"Message": "Order not found"}
