from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import ValidationError
from datetime import datetime
from jose import jwt, JWTError
from models import (
    User,
    SystemUser,
    UserAuth,
    UserOut,
    TokenPayload,
    token,
)
from utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    Algorithm,
    jwt_secret_key
)
from database import (
    engine,
)


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/Signup", response_model=UserOut, tags=["Sign up"])
async def register(data: UserAuth, session: Session = Depends(get_session)):
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


@router.post("/Login", summary="Create access and refresh tokens for user", response_model=token, tags=["Log in"])
async def Login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    existing_user = session.exec(statement).first()
    if existing_user is None:
        raise HTTPException(
            status_code=401, detail="Incorrect Username or password")
    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect Username or password")
    return {
        "access_token": create_access_token(existing_user.username),
        "refresh_token": create_refresh_token(existing_user.username)
    }
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/Login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), session: Session = Depends(get_session)) -> SystemUser:
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

    statement = select(User).where(User.username == token_data.sub)
    new_user = session.exec(statement).first()
    if new_user is None:
        raise HTTPException(status_code=400, detail="Could not find user")
    return new_user


@router.get("/Me/", summary="Get details of currently logged in user", response_model=UserOut, tags=["Information"])
async def get_me(user: User = Depends(get_current_user)):
    return user
