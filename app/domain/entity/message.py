from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, relationship

from app.domain.entity import Base


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True
    )
    cote_id: Mapped[str] = Column(String(36), ForeignKey('cote.id'), nullable=False)
    sender: Mapped[str] = Column(String(36), ForeignKey('user.id'), nullable=False)
    content: Mapped[str] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)

    cote: Mapped["Cote"] = relationship(
        "Cote", back_populates="messages", foreign_keys=[cote_id]
    )
