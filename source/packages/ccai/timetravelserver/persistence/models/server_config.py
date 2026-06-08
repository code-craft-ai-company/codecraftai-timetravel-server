from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from .base import Base, BaseMixin

class ServerConfiguration(BaseMixin, Base):
    __tablename__ = 'server_configuration'

    key: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
