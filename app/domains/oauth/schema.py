from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    user_token: str
    access_token: str
