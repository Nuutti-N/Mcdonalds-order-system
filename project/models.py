
from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class token(BaseModel):
    acces_token: str
    refresh_token: str
