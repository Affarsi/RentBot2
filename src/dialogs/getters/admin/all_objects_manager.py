from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput

from src.database.requests.object import db_get_object, db_delete_object, db_update_object
from src.database.requests.user import db_get_user, db_update_user
from src.dialogs.dialogs_states import CreateObject, UserDialog, AdminDialog
from src.utils.media_group_creator import create_media_group


# Возвращает количество всех объектов по типам
async def all_objects_count_getter(**kwargs):
    all_object_list = await db_get_object()

    status_mapping = {
        "🔄": "on_moderation_count",
        "✅": "submit_count",
        "❌": "deleted_count"
    }

    status_counts = {key: 0 for key in status_mapping.values()}

    for obj in all_object_list:
        status = obj.get("status")
        if status in status_mapping:
            status_counts[status_mapping[status]] += 1

    return status_counts


async def all_objects_count_and_sg_list_getter(**kwargs):
    all_object_list = await db_get_object()

    # Инициализируем словарь для истории
    result_summary = {
        "on_moderation_count": 0,
        "submit_count": 0,
        "deleted_count": 0,
        "deleted_objects_list": [],
        "confirmed_objects_list": [],
        "moderated_objects_list": []
    }

    # Обрабатываем объекты из списка
    for obj in all_object_list:
        status = obj.get("status")
        id = obj['id']
        generate_id = obj['generate_id']
        country = obj['country']

        if status == "🔄":
            result_summary["on_moderation_count"] += 1
            result_summary["moderated_objects_list"].append([f'{status} | ID: {generate_id} | {country}', str(id)])
        elif status == "✅":
            result_summary["submit_count"] += 1
            result_summary["confirmed_objects_list"].append([f'{status} | ID: {generate_id} | {country}', str(id)])
        elif status == "❌":
            result_summary["deleted_count"] += 1
            result_summary["deleted_objects_list"].append([f'{status} | ID: {generate_id} | {country}', str(id)])

    return result_summary


# Просмотр объекта со статусом "Удалено"
async def admin_open_object(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    # Сбор данных
    object_id = int(item_id)
    object_data = await db_get_object(object_id=object_id)
    object_data = object_data[0]
    chat_id = dialog_manager.event.message.chat.id

    # Сохраняем id открытого объета
    dialog_manager.dialog_data['admin_open_object_id'] = object_id

    # Создание media_group
    media_group = await create_media_group(dict_data=object_data)

    # Отправка media_group
    await dialog_manager.event.bot.send_media_group(
        chat_id=chat_id,
        media=media_group
    )

    # Чтобы медиа группа отправилась раньше чем смс от бота
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    # В зависимости от статуса выводим меню взаимодействия
    if object_data['status'] == '✅':
        await dialog_manager.switch_to(AdminDialog.admin_open_object_confirmed)
    elif object_data['status'] == '🔄':
        await dialog_manager.switch_to(AdminDialog.admin_open_object_moderated)
    else:
        await dialog_manager.switch_to(AdminDialog.admin_open_object_deleted)


# Инверсия переменной is_admin_edit_menu_open
async def invert_admin_edit_menu_open(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    is_admin_edit_menu_open = dialog_manager.dialog_data.get('is_admin_edit_menu_open', False)

    # Инверсируем значение
    dialog_manager.dialog_data['is_admin_edit_menu_open'] = not is_admin_edit_menu_open


# Инверсия переменной is_admin_delete_object_confirm_menu
async def invert_admin_dell_obj_confirm_menu(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    is_admin_delete_object_confirm_menu = dialog_manager.dialog_data.get('is_admin_delete_object_confirm_menu', False)

    # Инверсируем значение
    dialog_manager.dialog_data['is_admin_delete_object_confirm_menu'] = not is_admin_delete_object_confirm_menu


# Getter, сообщающий, открыто ли edit_menu/delete_menu или нет
async def admin_open_object_confirmed_getter(dialog_manager: DialogManager, **kwargs):
    is_edit_menu_open = dialog_manager.dialog_data.get('is_admin_edit_menu_open')
    is_delete_object_confirm_menu = dialog_manager.dialog_data.get('is_admin_delete_object_confirm_menu')
    return {'admin_dit_menu_open': is_edit_menu_open,
            'admin_delete_object_confirm_menu': is_delete_object_confirm_menu}


# Удалить созданный объект
async def admin_delete_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    object_id = dialog_manager.dialog_data.get('admin_open_object_id')

    # Изменяем статус объекта на 'Удалён'
    new_object_data = {'status': '❌'}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    # Оповещаем Администратора и отправляем в предыдущие окно
    await dialog_manager.event.answer('Объект успешно удалён!')
    await dialog_manager.switch_to(AdminDialog.all_objects_confirmed)