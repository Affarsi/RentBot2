from datetime import date
from sqlalchemy import select

from src.database.requests.user import db_get_user
from src.database.run_db import async_session
from src.database.models import Object, User, Country


# Добавляет новый объект
async def db_new_object(
        object_data: dict,
        user_tg_id: int
) -> bool or int:
    async with async_session() as session:
        # Определяем ID Пользователя в БД
        user = await db_get_user(telegram_id=user_tg_id)

        # Преобразования фотографий
        photo_list = object_data['create_object_state_data_photos']
        photo_str = ", ".join(photo_list)

        # Формирование объекта
        new_object = Object(
            status="🔄",
            generate_id=object_data['create_object_state_data_generate_id'],
            obj_type=object_data['create_object_state_data_type'],
            country_thread_id=object_data['create_object_state_data_country_thread_id'],
            address=object_data['create_object_state_data_address'],
            conditions=object_data['create_object_state_data_conditions'],
            description=object_data['create_object_state_data_description'],
            contacts=object_data['create_object_state_data_contacts'],
            photos=photo_str,
            payment_date=date.today(),
            owner_id=user["id"]
        )

        # Если объект бессрочной публикации
        if object_data.get('payment_date_no_limit', False):
            new_object.payment_date = None

        # Попытка добавления объекта в БД
        try:
            session.add(new_object)
            await session.commit()
            return True
        except Exception as e:
            print(f'При добавлении нового объекта в БД произошла ошибка:\n{e}')
            return False


# Извлекает объекты из базы данных на основе заданных параметров
async def db_get_object(
        object_id: int = None,
        country_thread_id: int = None,
        country_name: str = None,
        telegram_id: int = None,
        status: str = None
) -> list[dict]:
    """
    .

    Аргументы:
    - object_id (int, optional): ID объекта для фильтрации. Если указан, будут возвращены только объекты с этим ID.
    - country_name (str, optional): Имя страны для фильтрации объектов. Если указано, будут возвращены объекты, связанные с этой страной.
    - telegram_id (int, optional): ID Telegram для фильтрации объектов по владельцу. Если указан, будут возвращены объекты, принадлежащие этому владельцу.
    - status (str, optional): Статус объектов для фильтрации. Если указан, будут возвращены только объекты с этим статусом.

    Возвращает:
    - list: Список словарей, представляющих объекты из базы данных, соответствующие заданным критериям.
    """
    async with async_session() as session:
        # Начинаем запрос с соединения Object и Country
        query = select(Object, Country.name, Country.id, Country.thread_id).join(Country)

        if telegram_id is not None:
            # Сначала получаем user_id по telegram_id
            user_query = select(User.id).where(User.telegram_id == telegram_id)
            user_result = await session.execute(user_query)
            user_id = user_result.scalar()

            if user_id is not None:
                # Сортируем по owner_id и статусу
                query = query.where(Object.owner_id == user_id).order_by(Object.status)

        if object_id is not None:
            query = query.where(Object.id == object_id)
        elif country_name is not None:
            query = query.where(Country.name == country_name)
        elif country_thread_id is not None:  # Фильтруем по country_id, если он передан
            query = query.where(Object.country_thread_id == country_thread_id)

        if status is not None:
            # Если передан статус, фильтруем по статусу
            query = query.where(Object.status == status)

        result = await session.execute(query)
        objects = result.all()

        # Преобразуем объекты в список словарей
        objects_list = []
        for obj, country_name, country_id, country_thread_id in objects:
            objects_list.append({
                "id": obj.id,
                "generate_id": obj.generate_id,
                "status": obj.status,
                "obj_type": obj.obj_type,
                "country_id": country_id,
                "country": country_name,
                "country_thread_id": country_thread_id,
                "address": obj.address,
                "conditions": obj.conditions,
                "description": obj.description,
                "contacts": obj.contacts,
                "photos": obj.photos,
                "message_ids": obj.message_ids,
                "delete_reason": obj.delete_reason,
                "payment_date": obj.payment_date,
                "owner_id": obj.owner_id,
            })

        return objects_list


# Удаление объекта
async def db_delete_object(object_id: int):
    async with async_session() as session:
        obj = await session.execute(
            select(Object).where(Object.id == object_id)
        )
        obj = obj.scalar_one_or_none()

        if obj is None:
            return

        await session.delete(obj)
        await session.commit()


# Обновляет существующий объект
async def db_update_object(object_id: int, object_data: dict) -> bool:
    async with async_session() as session:
        # Получаем объект по его ID
        result = await session.execute(
            select(Object).where(Object.id == object_id)
        )
        obj = result.scalars().first()

        if not obj:
            print(f'Объект с ID {object_id} не найден в базе данных.')
            return False

        key_list = ['status', 'obj_type', 'country_thread_id', 'address', 'conditions', 'description', 'contacts', 'photos',
                    'delete_reason', 'message_ids']

        # Обновляем только указанные поля объекта
        for key, value in object_data.items():
            if key in key_list:
                if key == 'photos':
                    obj.photos = ", ".join(value) if isinstance(value, list) else value
                else:
                    setattr(obj, key, value)

        # Попытка сохранить изменения в БД
        try:
            await session.commit()
            return True
        except Exception as e:
            print(f'При обновлении объекта в БД произошла ошибка:\n{e}')
            return False