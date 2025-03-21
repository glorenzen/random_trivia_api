from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from app.db import get_db
from app.data.user import create, get_by_email, authenticate_user
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    User as UserSchema,
)
from app.schemas.token import Token, TokenData
from app.auth import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

router = APIRouter(prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create(db, user)
    return {"message": "Created new user", "user": new_user}


@router.get("/email", response_model=UserSchema)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_by_email(db, email)
    return UserSchema.model_validate(user, from_attributes=True)


@router.post("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/me/", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user
