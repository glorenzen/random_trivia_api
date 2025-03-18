from pydantic import BaseModel
from app.schemas.category import Category
from app.schemas.difficulty import Difficulty


class QuestionBase(BaseModel):
    question: str
    answer: str


class QuestionCreate(QuestionBase):
    category_name: str
    difficulty_level: str


class QuestionUpdate(QuestionBase):
    pass


class QuestionInDBBase(QuestionBase):
    id: int

    class Config:
        orm_mode: True


class Question(QuestionInDBBase):
    category: Category
    difficulty: Difficulty


class QuestionInDB(QuestionInDBBase):
    pass
