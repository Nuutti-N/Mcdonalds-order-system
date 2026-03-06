
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, select
from models import (
    User,
    UserOut,
)
from uuid import uuid4
from database import (
    engine
)
from users import get_current_user, router as users_router
from routers import router as orders_router

app = FastAPI()
app.include_router(users_router)
app.include_router(orders_router)


@app.get("/Welcome")
async def welcome_back():
    return {"Message": "Thank you for visiting, and welcome back."}
