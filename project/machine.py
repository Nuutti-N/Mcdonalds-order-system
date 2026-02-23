
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
order_list = []


class Order(BaseModel):
    id: int
    item: str
    status: str = "Pending"


@app.get("/")
async def basic_welcome_to_everyone():
    return {"Welcome to McDonald's Order system."}


@app.post("/order")
async def create_order(order: Order):
    order_list.append(order)
    return {"Message": "order added successfully", "order": order}


@app.get("/orders")
async def kitchen_display():
    return order_list
