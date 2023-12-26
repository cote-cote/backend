from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class CreateUserToken(BaseModel):
    id: str
    name: str
    email: str
    access_token: str


class OauthSignInUseCase(ABC):

    @abstractmethod
    def sign_in(self, auth_code: str) -> CreateUserToken:
        """Conduct OAuth sign-in with auth_code and get sign-in user's information.

        :param auth_code: The authentication code which is included in the redirected url after sign-in
        :return:
        """
        pass

    @abstractmethod
    def create_user_token(self, payload: Optional[CreateUserToken]) -> str:
        """Create user_token which is the counterpart of the access_token.

        :param payload: The properties of user would be used for creating user_token (ex. JWT)
        :return: The user_token paired with access_token
        """
        pass
