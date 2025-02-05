from sqlalchemy import select, func

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
        object_id: int = None,
        user_id: int = None
) -> dict | list | None:
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

        elif user_id is not None:
            # Пользователя по user_id
            user = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = user.scalar_one_or_none()

        else :
            # Получаем список всех пользователей в виде словарей
            user_results = await session.execute(select(User))
            users = user_results.scalars().all()
            users_list = []
            for user in users:
                users_list.append({
                    "id": user.id,
                    "telegram_id": user.telegram_id,
                    "full_name": user.full_name,
                    "username": user.username,
                    "status": user.status,
                    "object_limit": user.object_limit,
                    "balance": user.balance,
                    "recurring_payments": user.recurring_payments
                })

            user = users_list
            return user

        if user is None:
            return None  # Пользователь не найден

        # Получение ID объектов Пользователя
        objects = await session.execute(
            select(Object).where(Object.owner_id == user.id)
        )
        obj_list = [obj.id for obj in objects.scalars()]

        # Получение объектов Пользователя со статусами "🔄" и "✅"
        filtered_objects = await session.execute(
            select(Object).where(Object.owner_id == user.id, Object.status.in_(["🔄", "✅"]))
        )
        filtered_obj_list_len = len([obj.id for obj in filtered_objects.scalars()])

        # Подсчет бесплатных и платных объектов
        paid_objects_count = await session.execute(
            select(func.count(Object.id)).where(Object.owner_id == user.id, Object.payment_date != None)
        )
        free_objects_count = await session.execute(
            select(func.count(Object.id)).where(Object.owner_id == user.id, Object.payment_date == None,
                                                Object.status.in_(["🔄", "✅"]))
        )

        # Формируем словарь
        user_dict = {
            "id": str(user.id),
            "telegram_id": user.telegram_id,
            "full_name": user.full_name,
            "username": user.username,
            "status": user.status,
            "obj_limit": str(user.object_limit),
            "obj_list": obj_list,
            "obj_list_len": filtered_obj_list_len,
            "paid_objects_count": paid_objects_count.scalar(),
            "free_objects_count": free_objects_count.scalar(),
            "balance": user.balance,
            "recurring_payments": user.recurring_payments
        }

        return user_dict


# Изменить информацию о Пользователе
async def db_update_user(
        user_id: int = None,
        telegram_id: int = None,
        status: str = None,
        object_limit: int = None,
        plus_balance: int = None,
        recurring_payments: bool = None
):
    async with async_session() as session:
        # Получаем Пользователя по user_id
        if user_id is not None:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

        # Получаем Пользователя по telegram_id
        if telegram_id is not None:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()

        # Обновляем поля, если они были переданы
        if status is not None:
            user.status = status
        if object_limit is not None:
            user.object_limit = object_limit
        if plus_balance is not None:
            user.balance += plus_balance
        if recurring_payments is not None:
            user.recurring_payments = recurring_payments

        # Сохраняем изменения
        session.add(user)
        await session.commit()


# Поиск Пользователя по telegram username
async def find_user_by_username(username: str) -> int:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if user is not None:
            return user.id  # Возвращаем ID найденного пользователя
        return None  # Возвращаем None, если пользователь не найден