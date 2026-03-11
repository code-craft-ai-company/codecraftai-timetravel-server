from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Index
from .base import Base, BaseMixin
import datetime

class RegisteredProcess(BaseMixin, Base):
    __tablename__ = 'registered_processes'

    host: Mapped[str] = mapped_column(String(256), nullable=False)
    pid: Mapped[int] = mapped_column(Integer, nullable=False)
    application_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    pod_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    remote_control_address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    lifecycle_state: Mapped[str] = mapped_column(String(32), default="registered", nullable=False, index=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_heartbeat_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    disconnected_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index('ix_registered_processes_host_pid', 'host', 'pid'),
    )

    portal_snapshots: Mapped[List["PortalSnapshot"]] = relationship("PortalSnapshot", back_populates="process", cascade="all, delete-orphan")
    trace_sessions: Mapped[List["TraceSession"]] = relationship("TraceSession", back_populates="process", cascade="all, delete-orphan")
