from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.database.requests.object import db_get_object
from src.database.requests.user import db_get_user
from src.dialogs.dialogs_states import CreateObject


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
        my_object_list.append([f'{status} | ID: {generate_id} | {country}', {id}])

    return {'my_object_list': my_object_list}


# Запускает диалог с созданием объекта
async def start_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Сверка лимитов
    user_dict = await db_get_user(telegram_id=callback.from_user.id)
    obj_max = int(user_dict['obj_limit'])
    obj_len = user_dict['obj_list_len']

    # Пользователь не прошёл по лимитам
    if obj_len >= obj_max:
        await callback.answer('Ваш лимит исчерпан!')
        return

    await dialog_manager.start(CreateObject.get_country)