from datetime import datetime

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import Mapped, relationship

from app.legacy.db.models import Base
from app.utils.uuid import generate_uuid


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(String(36), default=generate_uuid, primary_key=True, nullable=False)
    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)

    owned_cotes: Mapped[list["Cote"]] = relationship(
        'Cote', back_populates='owner', foreign_keys='Cote.owner_id', cascade="all, delete-orphan"
    )
