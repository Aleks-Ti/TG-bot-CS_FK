from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(sa.String(64), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(sa.Integer, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(sa.String(64), nullable=True, unique=True)
    last_name: Mapped[str] = mapped_column(sa.String(64), nullable=True, unique=True)
    registered_at: Mapped[int] = mapped_column(sa.DateTime, default=datetime.now)

    game_profile = relationship("GameProfile", back_populates="user", uselist=False)


class GameProfile(Base):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="game_profile", uselist=False)
    guess_number = relationship("GuessNumber", back_populates="game_profile", uselist=False)
    binary_converter = relationship("BinaryConverter", back_populates="game_profile", uselist=False)
    haort_pyramid = relationship("HaortPyramid", back_populates="game_profile", uselist=False)


class GuessNumber(Base):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    best_result: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    total_number_games: Mapped[int] = mapped_column(
        sa.Integer, default=0, nullable=True, unique=False
    )
    game_profile = relationship("GameProfile", back_populates="guess_number", uselist=False)


class BinaryConverter(Base):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    total_try: Mapped[int] = mapped_column(
        sa.Integer, default=0, nullable=True, unique=False
    )
    count_encrypted_characters: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    number_decoded_characters: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)

    game_profile = relationship("GameProfile", back_populates="binary_converter", uselist=False)


class HaortPyramid(Base):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    total_number_games: Mapped[int] = mapped_column(
        sa.Integer, default=0, nullable=True, unique=False
    )

    game_profile = relationship("GameProfile", back_populates="haort_pyramid", uselist=False)
    game_difficulty = relationship(
        "DifficultyHaortPyramid", back_populates="haort_pyramid", uselist=True
    )


class DifficultyHaortPyramid(Base):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    game_difficulty: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    best_result: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)

    haort_pyramid = relationship("HaortPyramid", back_populates="game_difficulty", uselist=False)
