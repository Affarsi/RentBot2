from sqlalchemy import select, func, update

from src.database.requests.user import db_get_user
from src.database.run_db import async_session
from src.database.models import Object, User, Country


async def db_get_object(
        object_id: int = None,
        country_id: int = None,
        country_name: str = None,
        telegram_id: int = None,
        status: str = None
) -> list[dict]:
    """
    Извлекает объекты из базы данных на основе заданных параметров.

    Аргументы:
    - object_id (int, optional): ID объекта для фильтрации. Если указан, будут возвращены только объекты с этим ID.
    - country_name (str, optional): Имя страны для фильтрации объектов. Если указано, будут возвращены объекты, связанные с этой страной.
    - telegram_id (int, optional): ID Telegram для фильтрации объектов по владельцу. Если указан, будут возвращены объекты, принадлежащие этому владельцу.
    - status (str, optional): Статус объектов для фильтрации. Если указан, будут возвращены только объекты с этим статусом.

    Возвращает:
    - list: Список словарей, представляющих объекты из базы данных, соответствующие заданным критериям.
    """
    async with async_session() as session:
        query = select(Object, Country.name).join(Country)

        if telegram_id is not None:
            # Сначала получаем user_id по telegram_id
            user_query = select(User.id).where(User.telegram_id == telegram_id)
            user_result = await session.execute(user_query)
            user_id = user_result.scalar()

            if user_id is not None:
                # Теперь фильтруем объекты по owner_id
                query = query.where(Object.owner_id == user_id)

        if object_id is not None:
            query = query.where(Object.id == object_id)
        elif country_name is not None:
            query = query.where(Country.name == country_name)
        elif country_id is not None:  # Фильтруем по country_id, если он передан
            query = query.where(Object.country_id == country_id)

        if status is not None:
            # Если передан статус, фильтруем по статусу
            query = query.where(Object.status == status)

        result = await session.execute(query)
        objects = result.all()

        # Преобразуем объекты в список словарей
        objects_list = []
        for obj, country_name in objects:
            objects_list.append({
                "id": obj.id,
                'generate_id': obj.generate_id,
                "status": obj.status,
                "obj_type": obj.obj_type,
                "country_id": obj.country_id,
                "country": country_name,
                "address": obj.address,
                "conditions": obj.conditions,
                "description": obj.description,
                "contacts": obj.contacts,
                "photos": obj.photos,
                "owner_id": obj.owner_id,
            })

        return objects_list