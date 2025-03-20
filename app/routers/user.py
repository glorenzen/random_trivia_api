from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.user import create
from app.schemas.user import UserCreate, UserCreateResponse, User as UserSchema

router = APIRouter(prefix="/user")


@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create(db, user)
    return {"message": "Created new user", "user": new_user}
