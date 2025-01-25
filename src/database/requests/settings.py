from sqlalchemy import select, update

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


# Обновляем текст для раздела Информация
async def db_update_info(new_info: str) -> None:
    async with async_session() as session:
        async with session.begin():
            # Проверяем, существует ли запись в столбце info_text
            result = await session.execute(select(Setting.info_text))
            existing_info = result.scalars().first()

            if existing_info is not None:
                # Если запись существует, обновляем значение
                stmt = (
                    update(Setting)
                    .values(info_text=new_info)
                )
                await session.execute(stmt)
            else:
                # Если записи нет, создаем новую
                new_setting = Setting(info_text=new_info)
                session.add(new_setting)

        # Сохраняем изменения
        await session.commit()
