from abc import ABC, abstractmethod

from app.application.port.incoming.oauth_signin_use_case import UserInfo


class OauthPort(ABC):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    def get_oauth_access_code(self, auth_code: str) -> str:
        """Sign in with the authentication code and return the access token

        :param auth_code: The authentication code which is included in the redirected url after sign-in
        :return: The access token which oauth provider returned as a result of authorization
        """
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> UserInfo:
        """Get user info with the access token

        :param access_token: The token that oauth provider provided
        :return: User info that oauth provider provided
        """
        pass
