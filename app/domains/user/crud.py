from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models.user import User


class UserCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        user = User(
            name=name,
            email=email,
            password=password
        )
        self.db.add(user)
        return user

    def find_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email).one()
        return user
