
from pydantic import BaseModel
from sqlmodel import SQLModel


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
