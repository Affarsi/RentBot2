from aiogram_dialog import DialogManager

from src.database.requests.object import db_get_object
from src.database.requests.settings import db_get_info


# Возвращает текст для раздела Информация
async def my_objects_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.event.from_user.id
    object_list = await db_get_object(telegram_id=telegram_id)

    # Если у Пользователя не найдено объектов
    if not object_list:
        return {'my_object_list': [['У вас нет объектов', 1]]}

    # Формируем список объектов
    my_object_list = []

    for obj in object_list:
        id = obj['id']
        status = obj['status']
        generate_id = obj['generate_id']
        country = obj['country']
        my_object_list.append([f'{status} ID: {generate_id} | {country}', {id}])

    return {'my_object_list': my_object_list}