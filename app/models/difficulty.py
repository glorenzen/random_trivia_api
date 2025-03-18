from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base


class Difficulty(Base):
    __tablename__ = "difficulty"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, unique=True, index=True, nullable=False)
    questions = relationship("Question", back_populates="difficulty")
