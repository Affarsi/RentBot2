from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

# Пользователи
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default='Владелец')  # Владелец/Агент
    object_limit: Mapped[int] = mapped_column(default=1)
    balance: Mapped[int] = mapped_column(default=0)

# Страны
class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    thread_id: Mapped[int] = mapped_column(nullable=True)

# Объекты
class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    generate_id: Mapped[int]
    status: Mapped[str]
    obj_type: Mapped[str] = mapped_column(nullable=True)
    country_thread_id: Mapped[int] = mapped_column(ForeignKey('countries.thread_id'), nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    conditions: Mapped[str] = mapped_column(nullable=True) # Условия и цена
    description: Mapped[str] = mapped_column(nullable=True)
    contacts: Mapped[int] = mapped_column(nullable=True)
    photos: Mapped[str] = mapped_column(nullable=True)
    delete_reason: Mapped[str] = mapped_column(nullable=True)
    message_ids: Mapped[str] = mapped_column(nullable=True)

    # Связь с пользователем
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))  # Внешний ключ на пользователя

# Настройка бота
class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    info_text: Mapped[str] = mapped_column(nullable=True)