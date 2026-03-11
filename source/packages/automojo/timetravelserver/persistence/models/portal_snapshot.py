import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from .base import Base, BaseMixin

class PortalSnapshot(BaseMixin, Base):
    __tablename__ = 'portal_snapshots'

    process_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('registered_processes.id', ondelete='CASCADE'), nullable=False, index=True)
    portal_name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    snapshot_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    process: Mapped["RegisteredProcess"] = relationship("RegisteredProcess", back_populates="portal_snapshots")
