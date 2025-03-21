from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.data.user import create, get_by_email
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    User as UserSchema,
)

router = APIRouter(prefix="/user")


@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create(db, user)
    return {"message": "Created new user", "user": new_user}


@router.get("/email", response_model=UserSchema)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_by_email(db, email)
    return UserSchema.model_validate(user, from_attributes=True)


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    pass
