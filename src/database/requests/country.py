from sqlalchemy import select

from src.database.run_db import async_session
from src.database.models import Country


# Получить список всех стран
async def db_get_country() -> list:
    async with async_session() as session:
        # Выполняем запрос к базе данных для получения всех стран
        result = await session.execute(select(Country).order_by(Country.name))

        # Извлекаем данные из результата запроса
        countries = result.scalars().all()

        # Формируем список в формате [[ид страны, название страны, ид темы страны]]
        country_list = [[country.id, country.name, country.thread_id] for country in countries]

        return country_list


# Возращает название страны по её ID
async def db_get_country_name_by_id(country_id: int) -> str:
    async with async_session() as session:
        # Выполняем запрос к базе данных для получения страны по ID
        result = await session.execute(select(Country).where(Country.id == country_id))

        # Извлекаем единственный результат
        country = result.scalar_one_or_none()

        # Проверяем, была ли найдена страна, и возвращаем её название или сообщение об ошибке
        if country:
            return country.name
        else:
            return "Страна не найдена"