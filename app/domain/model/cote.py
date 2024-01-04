from datetime import datetime

from pydantic import BaseModel

from app.domain.model.repository import Repository
from app.domain.model.user import User


class Cote(BaseModel):
    problem_url: str
    repository: Repository
    participants: list[User] = []
    created_date: datetime
