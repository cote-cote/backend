from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    token: Optional[str]
    access_token: Optional[str]
