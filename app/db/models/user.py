import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import Mapped

from app.db.models import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(String(36), primary_key=True, default=uuid.uuid4(), nullable=False)
    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
