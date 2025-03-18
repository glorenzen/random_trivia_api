from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode: True


class Category(CategoryInDBBase):
    pass


class CategoryInDB(CategoryInDBBase):
    pass
