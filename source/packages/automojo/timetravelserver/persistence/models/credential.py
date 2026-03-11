from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from .base import Base, BaseMixin
import datetime

class Credential(BaseMixin, Base):
    __tablename__ = 'credentials'

    token_hash: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(128), nullable=False)
    last_used_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    revoked_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
