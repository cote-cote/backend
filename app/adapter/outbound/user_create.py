from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import entity
from app.domain import model
from app.port.incoming.oauth_signin_use_case import UserInfo
from app.port.outbound.user_create import UserCreatePort
from app.dependency.db import get_db


class UserCreateAdapter(UserCreatePort):

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_if_not_exist(self, user_info: UserInfo) -> model.User:
        try:
            user = self.db.query(entity.User).filter(entity.User.email == user_info.email).one()
        except NoResultFound:
            user = entity.User(
                name=user_info.name,
                email=user_info.email
            )
            self.db.add(user)
            self.db.flush()

        return model.User(
            id=user.id,
            name=user.name,
            email=user.email
        )

    def commit(self) -> bool:
        self.db.commit()
        return True
