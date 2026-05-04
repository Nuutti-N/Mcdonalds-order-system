from enum import Enum
# Here import BaseModel in from pydantic library. You will use these, if you have databases or API for your projects.
from pydantic import BaseModel
# Make SQLModel, Field, which I will tell more later.
from sqlmodel import SQLModel, Field


# Then we make class name of User, where we put SQLModel and make table to database.
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username:  str = Field(unique=True)
    password: str  # This will store hashed
    role: str = "User"


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    status: str = "Pending"
    price: float


class UserAuth(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(SQLModel):
    sub: str = None  # Username or Id
    exp: int = None  # Expiration
    role: str = "User"  # New: "admin", "guest", or "developer"


# This is what we actually return to the screen (NO password here!)
class SystemUser(SQLModel):
    id: int
    username: str


class Tags(Enum):
    item = "items"
    users = "users"
