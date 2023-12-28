from abc import ABC, abstractmethod


class TokenPort(ABC):
    @abstractmethod
    def encode(self, payload: dict[str, any]) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict[str, any]:
        pass
