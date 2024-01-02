import abc
from typing import Union


class SessionPort(abc.ABC):
    @abc.abstractmethod
    def put(self, key: str, value: Union[str, int, bool]) -> bool:
        pass

    @abc.abstractmethod
    def get(self, key: str) -> any:
        pass
