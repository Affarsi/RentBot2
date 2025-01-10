from sqlalchemy import select

from src.database.run_db import async_session
from src.database.models import User, Object


# Добавляем нового Пользователя
async def db_new_user(
    telegram_id: int,
    full_name: str,
    username: str
) -> bool:
    async with async_session() as session:
        # Пытаемся найти пользователя в БД
        user = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = user.scalar_one_or_none()

        # Добавляем пользователя в БД
        if user is None:
            new_user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username
            )
            session.add(new_user)
            await session.commit()
            return True

        # Обновляем актуальную информацию о пользователе
        if user.full_name != full_name or user.username != username:
            user.full_name = full_name
            user.username = username

            await session.commit()

        return False


# Возвращает информацию о Пользователе
async def db_get_user(
        telegram_id: int = None,
        object_id: int = None
) -> dict | None:
    async with async_session() as session:
        user = None

        if telegram_id is not None:
            # Получаем пользователя по telegram_id
            user = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = user.scalar_one_or_none()

        elif object_id is not None:
            # Получаем объект по object_id и затем его владельца
            object_result = await session.execute(
                select(Object).where(Object.id == object_id)
            )
            obj = object_result.scalar_one_or_none()

            if obj is not None:
                # Получаем пользователя по owner_id объекта
                user = await session.execute(
                    select(User).where(User.id == obj.owner_id)
                )
                user = user.scalar_one_or_none()

        if user is None:
            return None  # Пользователь не найден

        # Получение ID объектов Пользователя
        objects = await session.execute(
            select(Object).where(Object.owner_id == user.id)
        )
        obj_list = [obj.id for obj in objects.scalars()]

        # Формируем словарь
        user_dict = {
            "id": str(user.id),
            "telegram_id": user.telegram_id,
            "full_name": user.full_name,
            "username": user.username,
            "status": user.status,
            "obj_limit": str(user.object_limit),
            "obj_list": obj_list,
            "obj_list_len": len(obj_list)
        }

        return user_dict