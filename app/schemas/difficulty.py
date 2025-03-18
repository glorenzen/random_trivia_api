from pydantic import BaseModel


class DifficultyBase(BaseModel):
    level: str


class DifficultyCreate(DifficultyBase):
    pass


class DifficultyUpdate(DifficultyBase):
    pass


class DifficultyInDBBase(DifficultyBase):
    id: int

    class Config:
        orm_mode: True


class Difficulty(DifficultyInDBBase):
    pass


class DifficultyInDB(DifficultyInDBBase):
    pass
