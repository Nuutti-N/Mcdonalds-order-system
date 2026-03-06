
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username:  str = Field(unique=True)
    password: str  # This will store hashed


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


class token(BaseModel):
    acces_token: str
    refresh_token: str


class TokenPayload(SQLModel):
    sub: str = None  # Username or Id
    exp: int = None  # Expiration
    role: str = "User"  # New: "admin", "guest", or "developer"


# This is what we actually return to the screen (NO password here!)
class SystemUser(SQLModel):
    id: int
    username: str
