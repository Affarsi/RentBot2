from sqlalchemy import select

from src.database.run_db import async_session
from src.database.models import User


# Добавляем нового Пользователя
async def db_new_user(
    telegram_id: int,
    full_name: str,
    username: str,
    invite_date: str
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
                username=username,
                invite_date=invite_date
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


# Возращает информацию о Пользователе
async def db_get_user(telegram_id: int) -> dict[str]:
    async with async_session() as session:
        # Получаем Пользователя
        user = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = user.scalar_one_or_none()

        # Формируем словарь
        user_dict = {
            "id": str(user.id),
            "full_name": user.full_name,
            "username": user.username,
            "points_balance": str(user.points_balance),
            "referrals_count": str(user.referrals_count),
            "invite_date": user.invite_date
        }

        return user_dict