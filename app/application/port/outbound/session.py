from abc import ABC, abstractmethod
from typing import Union


class SessionPort(ABC):
    @abstractmethod
    def put(self, key: str, value: Union[str, int, bool]) -> bool:
        pass
