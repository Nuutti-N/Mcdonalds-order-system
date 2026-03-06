
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, select
from models import (
    User,
    Order,
    UserOut,
    UserAuth,
    token,
    TokenPayload,
    SystemUser
)
from utils import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    Algorithm,
    jwt_secret_key
)
from users import (
    get_current_user
)
from uuid import uuid4
from database import (
    engine
)


app = FastAPI()


@app.get("/Me/", summary="Get details of currently logged in user", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@app.get("/")
async def basic_welcome_to_everyone():
    return {"Message": "Welcome to McDonald's Order system."}


@app.get("/Welcome")
async def welcome_back():
    return {"Message": "Thank you for visiting, and welcome back."}
