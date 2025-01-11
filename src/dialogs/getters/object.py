from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select

from src.database.requests.object import db_get_object, db_delete_object, db_update_object
from src.database.requests.user import db_get_user
from src.dialogs.dialogs_states import CreateObject, UserDialog
from src.utils.media_group_creator import create_media_group


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
        my_object_list.append([f'{status} | ID: {generate_id} | {country}', str(id)])

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


# Вывод информации об объекте Пользователю с меню взаимодействия
async def open_my_object(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    dialog_manager.dialog_data['open_object_id'] = int(item_id) # id открытого объекта
    object_id = int(item_id)
    object_data = await db_get_object(object_id=object_id)
    object_data = object_data[0]
    chat_id = dialog_manager.event.message.chat.id

    # Формирование медиа группы
    media_group = await create_media_group(dict_data=object_data)

    # Отправка медиа группы
    await dialog_manager.event.bot.send_media_group(
        chat_id=chat_id,
        media=media_group
    )

    # Чтобы медиа группа отправилась раньше чем смс от бота
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    # В зависимости от статуса выводим меню взаимодействия
    if object_data['status'] == '✅':
        await dialog_manager.switch_to(UserDialog.open_my_object_confirmed)
    elif object_data['status'] == '🔄':
        await dialog_manager.switch_to(UserDialog.open_my_object_moderated)
    else:
        await dialog_manager.switch_to(UserDialog.open_my_object_deleted)


# Удалить созданный объект
async def delete_my_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    object_id = dialog_manager.dialog_data.get('open_object_id')

    # Изменяем статус объекта на 'Удалён'
    new_object_data = {'status': '❌'}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    await dialog_manager.event.answer('Объект успешно удалён!')
    await dialog_manager.back()


# Открывает или закрывает edit_menu


# Getter, сообщающий, открыто ли edit_menu или нет
async def object_confirmed_getter(dialog_manager: DialogManager, **kwargs):
    is_edit_menu_open = dialog_manager.dialog_data.get('is_edit_menu_open')
    return {'edit_menu_open': is_edit_menu_open}