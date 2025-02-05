from sqlalchemy import select, delete

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


# Возвращает название страны по её thread_ID
async def db_get_country_name_by_thread_id(country_thread_id: int) -> str:
    async with async_session() as session:
        # Выполняем запрос к базе данных для получения страны по ID
        result = await session.execute(select(Country).where(Country.thread_id == country_thread_id))

        # Извлекаем единственный результат
        country = result.scalar_one_or_none()

        # Проверяем, была ли найдена страна, и возвращаем её название или сообщение об ошибке
        if country:
            return country.name
        else:
            return "Страна не найдена"


# Добавить новые страны по списку
async def db_update_countries(country_list: list[list[str, int]]) -> None:
    async with async_session() as session:
        # Очищаем таблицу стран
        await session.execute(delete(Country))

        # Создаем страны из переданного списка
        for country_name, thread_id in country_list:
            new_country = Country(name=country_name, thread_id=thread_id)
            session.add(new_country)

        await session.commit()  # Фиксируем изменения в базе данных