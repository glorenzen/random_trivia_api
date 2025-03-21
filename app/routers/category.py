from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.data.category import create, get_all, get_one
from app.schemas.category import CategoryCreate, Category as CategorySchema

router = APIRouter(prefix="/categories")


@router.get("/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)) -> List[CategorySchema]:
    return get_all(db)


@router.get("/{name}", response_model=CategorySchema)
def get_category(name: str, db: Session = Depends(get_db)):
    return get_one(db, category_name=name)


@router.post("/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create(db, category)
