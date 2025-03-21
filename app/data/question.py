from typing import List

from fastapi import HTTPException, status
from app.models.question import Question
from app.models.category import Category
from app.models.difficulty import Difficulty
from app.schemas.question import QuestionCreate, Question as QuestionSchema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func


def get_all(db: Session) -> List[QuestionSchema]:
    questions = db.query(Question).all()
    return [
        QuestionSchema.model_validate(question, from_attributes=True)
        for question in questions
    ]


def get_random(
    db: Session,
    category: List[str] = None,
    difficulty: List[str] = None,
    count: int = 10,
) -> List[QuestionSchema]:
    query = db.query(Question)

    # If a category/categories are provided, filter by it
    if category:
        query = query.join(Question.category).filter(
            Question.category.has(Category.name.in_(category))
        )

    # If a difficulty/difficulties are provided, filter by it
    if difficulty:
        query = query.join(Question.difficulty).filter(
            Question.difficulty.has(Difficulty.level.in_(difficulty))
        )

    # Fetch random questions and limit to the number
    questions = query.order_by(func.random()).limit(count).all()

    return [
        QuestionSchema.model_validate(question, from_attributes=True)
        for question in questions
    ]


def get_one_by_id(db: Session, id: int):
    question = db.query(Question).filter_by(id=id).first()
    return QuestionSchema.model_validate(question, from_attributes=True)


def create(db: Session, question: QuestionCreate) -> QuestionSchema:
    # Get or create the category
    category = (
        db.query(Category).filter(Category.name == question.category_name).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{question.category_name}' does not exist",
        )

    # Get or create the difficulty
    difficulty = (
        db.query(Difficulty)
        .filter(Difficulty.level == question.difficulty_level)
        .first()
    )
    if not difficulty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Difficulty '{question.difficulty_level}' does not exist",
        )

    # Create the question
    db_question = Question(
        question=question.question,
        answer=question.answer,
        category=category,
        difficulty=difficulty,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    db.delete(question)
    db.commit()
    return {
        "message": "Question deleted successfully",
        "question_id": question.id,
    }
