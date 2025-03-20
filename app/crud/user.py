from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from sqlalchemy.orm import Session
from app.auth import get_password_hash, verify_password


def create(db: Session, user: UserCreate):
    pw_hash = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        disabled=user.disabled,
        hashed_password=pw_hash,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
