from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass


# Информация о Пользователе
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    points_balance: Mapped[int] = mapped_column(default=0)  # Баллы
    lvl_number: Mapped[int] = mapped_column(ForeignKey('lvls.number')) # Уровень
    rank_title: Mapped[str] = mapped_column(ForeignKey('ranks.title')) # Звание
    referrals_count: Mapped[int] = mapped_column(default=0)
    invite_date: Mapped[str] = mapped_column(nullable=True)

    lvl = relationship("Lvl", back_populates="users")
    rank = relationship("Rank", back_populates="users")


# Информация об уровнях
class Lvl(Base):
    __tablename__ = "lvls"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]
    min_points: Mapped[int]
    max_points: Mapped[int]

    users = relationship("User", back_populates="lvl")


# Информация о званиях
class Rank(Base):
    __tablename__ = "ranks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    min_lvl: Mapped[int]
    max_lvl: Mapped[int]

    users = relationship("User", back_populates="rank")

