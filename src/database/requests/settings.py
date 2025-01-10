from sqlalchemy import select

from src.database.run_db import async_session
from src.database.models import Setting


# Получаем текст для раздела Информация
async def db_get_info() -> str:
    async with async_session() as session:
        # Пытаемся найти пользователя в БД
        info = await session.execute(
            select(Setting.info_text)
        )
        info = info.scalar_one_or_none()

        return info
