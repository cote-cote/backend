import abc


class TokenPort(abc.ABC):
    @abc.abstractmethod
    def encode(self, payload: dict[str, any]) -> str:
        pass

    @abc.abstractmethod
    def decode(self, token: str) -> dict[str, any]:
        pass

    @abc.abstractmethod
    def get_user_id(self, token: str) -> str:
        pass
