from typing import List
from app.models.category import Category
from app.schemas.category import CategoryCreate, Category as CategorySchema
from sqlalchemy.orm import Session


def create(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_all(db: Session) -> List[CategorySchema]:
    categories = db.query(Category).all()
    return [
        CategorySchema.model_validate(category, from_attributes=True)
        for category in categories
    ]


def get_one(db: Session, category_name: str):
    category = db.query(Category).filter(Category.name == category_name).first()
    return CategorySchema.model_validate(category, from_attributes=True)
