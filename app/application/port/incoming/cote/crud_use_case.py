from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.adapter.incoming.web.schema.response.cote import CoteResponse


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
    def get_cotes(self, cote_read: CoteRead) -> list[CoteResponse]:
        pass

    @abstractmethod
    def get_cote(self, cote_id: str) -> CoteResponse:
        pass

    @abstractmethod
    def create_cote(self, cote_create: CoteCreate) -> CoteResponse:
        pass

    @abstractmethod
    def update_cote(self, cote_id: str, user_id: str, cote_update: CoteUpdate) -> CoteResponse:
        pass

    @abstractmethod
    def delete_cote(self, cote_id: str, user_id: str) -> bool:
        pass
