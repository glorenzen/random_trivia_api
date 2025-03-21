from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.data.question import create, get_all, get_random, get_one_by_id, delete
from app.schemas.question import QuestionCreate, Question as QuestionSchema

router = APIRouter(prefix="/questions")


@router.get("/", response_model=List[QuestionSchema])
def get_questions(db: Session = Depends(get_db)) -> List[QuestionSchema]:
    return get_all(db)


@router.get("/random", response_model=List[QuestionSchema])
def get_random_questions(
    category: Optional[List[str]] = Query(None),
    difficulty: Optional[List[str]] = Query(None),
    count: int = 10,
    db: Session = Depends(get_db),
):
    """
    Fetches random trivia questions based on params.
    """

    return get_random(db, category, difficulty, count)


# @router.get("/{name}", response_model=QuestionSchema)
# def get_category(name: str, db: Session = Depends(get_db)):
#     return get_one(db, category_name=name)


@router.get("/{id}", response_model=QuestionSchema)
def get_question_by_id(id: int, db: Session = Depends(get_db)):
    return get_one_by_id(db, id)


@router.post("/", response_model=QuestionSchema)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return create(db, question)


@router.delete("/{id}")
def delete_question(id: int, db: Session = Depends(get_db)) -> dict:
    return delete(db, question_id=id)
