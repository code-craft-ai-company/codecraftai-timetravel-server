import uuid
import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from .base import Base, BaseMixin

class TraceSession(BaseMixin, Base):
    __tablename__ = 'trace_sessions'

    process_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('registered_processes.id', ondelete='CASCADE'), nullable=False, index=True)
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    stopped_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False, index=True)
    data_reference: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    process: Mapped["RegisteredProcess"] = relationship("RegisteredProcess", back_populates="trace_sessions")
