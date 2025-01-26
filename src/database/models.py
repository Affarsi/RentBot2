from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from datetime import date

class Base(AsyncAttrs, DeclarativeBase):
    pass

# Пользователи
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    full_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    status: Mapped[str] = mapped_column(default='Владелец')  # Владелец/Агент
    object_limit: Mapped[Optional[int]] = mapped_column(default=1)
    balance: Mapped[int] = mapped_column(default=0)

    # Связь с Платежами
    payments: Mapped[List["PaymentHistory"]] = relationship(back_populates="user")

# Страны
class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    thread_id: Mapped[int]

# Объекты
class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    generate_id: Mapped[Optional[int]]
    status: Mapped[Optional[str]]
    obj_type: Mapped[Optional[str]]
    country_thread_id: Mapped[Optional[int]] = mapped_column(ForeignKey('countries.thread_id'))
    address: Mapped[Optional[str]]
    conditions: Mapped[Optional[str]] # Условия и цена
    description: Mapped[Optional[str]]
    contacts: Mapped[Optional[str]]
    photos: Mapped[Optional[str]]
    delete_reason: Mapped[Optional[str]]
    message_ids: Mapped[Optional[str]]
    create_data: Mapped[date] = mapped_column(default=date.today())

    # Связь с Пользователем
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)  # Внешний ключ на пользователя

# Настройка бота
class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    info_text: Mapped[Optional[str]]

# История платежей
class PaymentHistory(Base):
    __tablename__ = "payments_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    order_id: Mapped[Optional[str]]
    amount: Mapped[Optional[int]]
    datetime: Mapped[Optional[date]] = mapped_column(default=date.today())
    success: Mapped[Optional[bool]] = mapped_column(default=False)

    # Связь с Пользователем
    user: Mapped["User"] = relationship(back_populates="payments")