import abc

from app.entity import Cote
from app.port.incoming.cote.crud_use_case import CoteCreate, CoteUpdate


class CoteCrudPort(abc.ABC):
    @abc.abstractmethod
    def find_cotes(self, page: int, per_page: int) -> list[Cote]:
        pass

    @abc.abstractmethod
    def find_cote_by_id(self, cote_id: str) -> Cote:
        pass

    @abc.abstractmethod
    def create_cote(self, cote_create: CoteCreate) -> Cote:
        pass

    @abc.abstractmethod
    def update_cote(self, cote: Cote, cote_update: CoteUpdate) -> Cote:
        pass

    @abc.abstractmethod
    def delete_cote(self, cote: Cote) -> bool:
        pass

    @abc.abstractmethod
    def commit(self) -> bool:
        pass
