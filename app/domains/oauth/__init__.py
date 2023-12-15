from abc import ABC, abstractmethod

from fastapi import Depends

from app.configs import Settings, get_settings
from app.domains.oauth.schema import UserInfo


def get_client_id(settings: Settings = Depends(get_settings)):
    return settings.GITHUB_CLIENT_ID


def get_client_secret(settings: Settings = Depends(get_settings)):
    return settings.GITHUB_CLIENT_SECRET


class OauthProvider(ABC):
    @abstractmethod
    def get_access_token(self, auth_code: str) -> str:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> UserInfo:
        pass
