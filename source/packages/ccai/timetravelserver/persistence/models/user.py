from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base, BaseMixin

class User(BaseMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    role: Mapped[str] = mapped_column(String(32), default="viewer", nullable=False)
