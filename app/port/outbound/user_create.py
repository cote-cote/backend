from abc import ABC, abstractmethod

from app.port.outbound.oauth import UserInfo
from app.domain.model.user import User


class UserCreatePort(ABC):
    @abstractmethod
    def create_if_not_exist(self, user_info: UserInfo) -> User:
        pass

    @abstractmethod
    def commit(self) -> bool:
        pass
