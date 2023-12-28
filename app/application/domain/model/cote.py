from datetime import datetime

from pydantic import BaseModel

from app.application.domain.model.repository import Repository
from app.application.domain.model.user import User


class Cote(BaseModel):
    problem_url: str
    repository: Repository
    participants: list[User] = []
    created_date: datetime
