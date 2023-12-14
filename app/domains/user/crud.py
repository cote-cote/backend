from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models.user import User
from app.exceptions import BadRequestException
from app.exceptions.error_code import ErrorCode


class UserCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find_user_by_email(self, email: str) -> User:
        try:
            user = self.db.query(User).filter(User.email == email).one()
            return user
        except NoResultFound:
            raise BadRequestException(
                message=f"No user exists: email: {email}",
                error_code=ErrorCode.USER_NOT_EXISTS
            )

    def save_user(self, user: User) -> User:
        self.db.add(user)
