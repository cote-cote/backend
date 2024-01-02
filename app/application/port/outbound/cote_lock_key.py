import abc


class CoteLockKeyPort(abc.ABC):
    @abc.abstractmethod
    def generate_key(self, key_id: str) -> str:
        pass
