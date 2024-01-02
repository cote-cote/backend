from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.application.entity import Cote


class CoteResponse(BaseModel):
    cote_id: str
    cote_name: str
    cote_problem_url: str
    cote_capacity: int
    cote_created_date: datetime
    cote_updated_date: datetime
