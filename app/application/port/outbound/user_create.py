from abc import ABC, abstractmethod

from app.application.port.outbound.oauth import UserInfo
from app.application.domain.model.user import User


class UserCreatePort(ABC):
    @abstractmethod
    def create_if_not_exist(self, user_info: UserInfo) -> User:
        pass

    @abstractmethod
    def commit(self) -> bool:
        pass
