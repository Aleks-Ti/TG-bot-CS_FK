from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(sa.String(64), nullable=False, unique=True)
    tg_user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(sa.String(64), nullable=True, unique=True)
    last_name: Mapped[str] = mapped_column(sa.String(64), nullable=True, unique=True)
    registered_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now)

    game_profile = relationship("GameProfile", back_populates="user", uselist=False)
