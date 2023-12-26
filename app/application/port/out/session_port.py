from abc import ABC, abstractmethod


class SessionPort(ABC):
    @abstractmethod
    def store_token_pair_into_session(self, user_token: str, access_token: str) -> bool:
        """Store the token pair into the session.

        :param user_token: The token client will be using
        :param access_token: The access token which oauth provider returned as a result of authorization
        :return:
        """
        pass
