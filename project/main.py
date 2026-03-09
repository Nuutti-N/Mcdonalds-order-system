
from fastapi import FastAPI, HTTPException, Depends, status
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

# Here we make variables (app) and we import FastAPI from the fastapi library, so we put FastAPI().
app = FastAPI()
app.include_router(users_router)
app.include_router(orders_router)


@app.get("/Welcome", tags=["Welcome"])
# asyn def allos handling multiple request simultaneously without waiting.
async def welcome_back():
    # Return message.
    return {"Message": "Thank you for visiting, and welcome back."}
