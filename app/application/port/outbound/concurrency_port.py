import abc
from typing import Generator


class ConcurrencyPort(abc.ABC):
    @abc.abstractmethod
    def lock(self, key: str) -> Generator:
        """
        Yield lock object.
        Both lock and lock session must be close after finished transaction.
        """
        pass
