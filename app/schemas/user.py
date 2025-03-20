from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None


class UserCreate(UserBase):
    password: str


class UserCreateResponse(BaseModel):
    message: str
    user: UserBase


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode: True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
