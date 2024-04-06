import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.user.models import User  # noqa


class GameProfile(Base):
    __tablename__ = "game_profile"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="game_profile", uselist=False)

    guess_number = relationship("GuessNumber", back_populates="game_profile", uselist=False)
    binary_converter = relationship("BinaryConverter", back_populates="game_profile", uselist=False)
    game_profile_haort_pyramid = relationship("GameProfileHaortPyramid", back_populates="game_profile", uselist=False)


class GuessNumber(Base):
    __tablename__ = "guess_number"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    best_result: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    total_number_games: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    game_profile_id: Mapped[int] = mapped_column(sa.ForeignKey("game_profile.id"), nullable=False, unique=True)

    game_profile = relationship("GameProfile", back_populates="guess_number", uselist=False)


class BinaryConverter(Base):
    __tablename__ = "binary_converter"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    total_try_convert_word_in_byte: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    total_try_convert_byte_in_word: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    count_encrypted_characters: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    count_encrypted_word: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    number_decoded_characters: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    number_decoded_word: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)
    game_profile_id: Mapped[int] = mapped_column(sa.ForeignKey("game_profile.id"), nullable=False, unique=True)

    game_profile = relationship("GameProfile", back_populates="binary_converter", uselist=False)


class GameProfileHaortPyramid(Base):
    __tablename__ = "game_profile_haort_pyramid"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    game_difficulty: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    haort_pyramid_id: Mapped[int] = mapped_column(sa.ForeignKey("haort_pyramid.id"), nullable=False, unique=True)
    game_profile_id: Mapped[int] = mapped_column(sa.ForeignKey("game_profile.id"), nullable=False, unique=True)

    game_profile = relationship("GameProfile", back_populates="game_profile_haort_pyramid", uselist=False)
    haort_pyramid = relationship("HaortPyramid", back_populates="game_profile_haort_pyramid", uselist=True)


class HaortPyramid(Base):
    __tablename__ = "haort_pyramid"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
    best_result: Mapped[int] = mapped_column(sa.Integer, nullable=True, unique=False)
    total_number_games: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True, unique=False)

    game_profile_haort_pyramid = relationship("GameProfileHaortPyramid", back_populates="haort_pyramid", uselist=True)
