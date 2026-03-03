
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from passlib.context import CryptContext
from project.utils import create_acces_token, create_refresh_token

app = FastAPI()

engine = create_engine("sqlite:///./project/mcd-order.db")
SQLModel.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username:  str = Field(unique=True)
    password: str  # This will store hashed


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    status: str = "Pending"
    price: float


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/register")
async def register(username: str, password: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username exists")

        hashed_pw = hash_password(password)
        new_user = User(username=username, password=hashed_pw)
        session.add(new_user)
        session.commit()
    return {"message": "User registered"}


@app.get("/")
async def basic_welcome_to_everyone():
    return {"Message": "Welcome to McDonald's Order system."}


@app.get("/Welcome")
async def welcome_back():
    return {"Message": "Thank you for visiting, and welcome back."}


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
async def one_order(order_id: int):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        results = session.exec(statement)
        order = results.first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return order
