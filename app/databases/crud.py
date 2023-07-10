from typing import Type

from sqlalchemy.orm import Session

from app.models.relational import User


def create_user(db: Session, user: User) -> User:
    if user.id:
        return update_user(db, user)
    else:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, user_name: str) -> User | None:
    return db.query(User).filter(User.username == user_name).first()


def update_user(db: Session, user: User) -> User | None:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    db.delete(get_user(db, user_id))
    db.commit()
