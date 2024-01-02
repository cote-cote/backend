from abc import ABC, abstractmethod

from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    email: str
    access_token: str


class OauthSignInUseCase(ABC):

    @abstractmethod
    def sign_in(self, auth_code: str) -> str:
        """Conduct OAuth sign-in with auth_code and get sign-in user's information.

        :param auth_code: The authentication code which is included in the redirected url after sign-in
        :return: Generated user_token
        """
        pass
