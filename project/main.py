
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import RedirectResponse
from models import UserOut, UserAuth, token
from utils import (
    hash_password,
    create_acces_token,
    create_refresh_token,
    verify_password,
    Algorithm,
    jwt_secret_key
)
from uuid import uuid4
from typing import Union, Any
from datetime import datetime
from jose import jwt, JWTError
from pydantic import ValidationError
from models import TokenPayload, SystemUser
import os
from dotenv import load_dotenv
load_dotenv()


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username:  str = Field(unique=True)
    password: str  # This will store hashed


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    status: str = "Pending"
    price: float


app = FastAPI()

engine = create_engine(os.getenv("DataBase_URL"))
SQLModel.metadata.create_all(engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/Singup/", response_model=UserOut)
async def register(data: UserAuth):
    with Session(engine) as session:
        statement = select(User).where(User.username == data.username)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username exists")

        hashed_pw = hash_password(data.password)
        new_user = User(username=data.username,
                        password=hashed_pw)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


@app.post("/Login", summary="Create access and refresh tokens for user", response_model=token)
async def Login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        statement = select(User).where(User.username == form_data.username)
        existing_user = session.exec(statement).first()
        if existing_user is None:
            raise HTTPException(
                status_code=400, detail="Incorrect Username or password")

        if not verify_password(form_data.password, existing_user.password):
            raise HTTPException(
                status_code=400, detail="Incorrect Username or password")
    return {
        "acces_token": create_acces_token(existing_user.username),
        "refresh_token": create_refresh_token(existing_user.username)
    }
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/Login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, jwt_secret_key, algorithms=[Algorithm]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=401, detail="Token Expired", headers={
                                "WWW-Authenticate": "Bearer"})
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials", headers={
                            "WWW-Authenticate": "Bearer"})

    with Session(engine) as session:
        statement = select(User).where(User.username == token_data.sub)
        new_user = session.exec(statement).first()
    if new_user is None:
        raise HTTPException(status_code=400, detail="Could not find user")
    return new_user


@app.get("/Me/", summary="Get details of currently logged in user", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


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
async def one_order(order_id: int):
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
