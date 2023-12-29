from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.domain.model import Cote


class CoteRead(BaseModel):
    page: int = 1
    per_page: int = 10


class CoteCreate(BaseModel):
    name: str
    owner_id: str
    problem_url: str
    capacity: int


class CoteUpdate(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[str] = None
    capacity: Optional[int] = None


class CoteCrudUseCase(ABC):
    @abstractmethod
    def get_cotes(self, cote_read: CoteRead) -> list[Cote]:
        pass

    @abstractmethod
    def get_cote(self, cote_id: str) -> Cote:
        pass

    @abstractmethod
    def create_cote(self, cote_create: CoteCreate) -> Cote:
        pass

    @abstractmethod
    def update_cote(self, cote_id: str, user_id: str, update_cote: CoteUpdate) -> Cote:
        pass

    @abstractmethod
    def delete_cote(self, cote_id: str, user_id: str) -> bool:
        pass
