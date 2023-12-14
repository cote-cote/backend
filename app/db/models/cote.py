import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.db.models import Base


class Cote(Base):
    __tablename__ = 'cote'

    id: Mapped[int] = Column(String(36), primary_key=True, default=uuid.uuid4(), nullable=False)
    owner_id: Mapped[str] = Column(String(36), ForeignKey('user.id'), nullable=False)
    name: Mapped[str] = Column(String(255), nullable=False)
    problem_url: Mapped[str] = Column(String(500), nullable=False)
    capacity: Mapped[str] = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)

    owner: Mapped["User"] = relationship(
        "User", back_populates="owned_cotes", foreign_keys=[owner_id]
    )

    messages: Mapped[list["Message"]] = relationship(
        'Message', back_populates='cote', foreign_keys='Message.cote_id', cascade="all, delete-orphan"
    )
