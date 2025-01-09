from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

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
    object_limit: Mapped[int] = mapped_column(default=5)

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
    status: Mapped[str]
    obj_type: Mapped[str] = mapped_column(nullable=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    conditions: Mapped[str] = mapped_column(nullable=True) # Условия и цена
    description: Mapped[str] = mapped_column(nullable=True)
    contacts: Mapped[int] = mapped_column(nullable=True)
    photos: Mapped[str] = mapped_column(nullable=True)

    # Связь с пользователем
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))  # Внешний ключ на пользователя

    # Связь с постами
    posts: Mapped[list['Post']] = relationship("Post", back_populates="object", cascade="all, delete-orphan")

# Созданные посты
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int]
    thread_id: Mapped[int]

    # Внешний ключ на объект
    object_id: Mapped[int] = mapped_column(ForeignKey('objects.id'))  # Внешний ключ на объект
    object: Mapped[Object] = relationship("Object", back_populates="posts")