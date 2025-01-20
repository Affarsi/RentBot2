from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput

from config import Config
from src.database.requests.object import db_get_object, db_update_object
from src.dialogs.dialogs_states import AdminDialog
from src.utils.media_group_creator import send_media_group


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


# геттер, возвращает количество объектов по статусу, а также списки этих объектов для scrolling group
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


# Функция просмотра открытого объекта (отправки media_group)
async def admin_open_object(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    # Сбор данных
    object_id = int(item_id)
    chat_id = dialog_manager.event.message.chat.id

    # Отправка медиа группы
    object_data = await send_media_group(dialog_manager, object_id, chat_id)

    # Сохраняем id и data открытого объета
    dialog_manager.dialog_data['admin_open_object_id'] = object_id
    dialog_manager.dialog_data['admin_open_object_data'] = object_data

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
async def admin_edit_and_delete_menu_getter(dialog_manager: DialogManager, **kwargs):
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
    object_data = dialog_manager.dialog_data.get('admin_open_object_data')

    # Удаление поста с группы
    message_ids = object_data['message_ids']
    message_ids = message_ids.split(', ')
    await dialog_manager.event.bot.delete_messages(chat_id=Config.chat, message_ids=message_ids)

    # Изменяем статус объекта на 'Удалён'
    new_object_data = {'status': '❌'}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    # Оповещаем Администратора и отправляем в предыдущие окно
    await dialog_manager.event.answer('Объект успешно удалён!')
    await dialog_manager.switch_to(AdminDialog.all_objects_confirmed)


# Одобрить объект, находящийся на модерации
async def accept_moderated_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Формируем данные
    object_id = dialog_manager.dialog_data.get('admin_open_object_id')
    chat_id = Config.chat
    send_to_chat = True # отправляем пост в группу, а не в лс

    # Отправляем пост в группу
    object_data = await send_media_group(dialog_manager, object_id, chat_id, send_to_chat)

    if not object_data:
        await dialog_manager.event.answer('Ошибка при отправки поста. Обратитесь к тех администратору!')
        return

    # Изменяем статус объекта на 'Одобрен'
    new_object_data = {'status': '✅', 'message_ids': object_data.get('message_ids')}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    # Оповещаем Администратора и отправляем в предыдущие окно
    await dialog_manager.event.answer('Объект успешно одобрен!\nСегодня вы в ударе :)')
    await dialog_manager.switch_to(AdminDialog.all_objects_moderated)


# Отклонить объект, находящийся на модерации
async def reason_object_reject_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    delete_reason = message.html_text
    object_id = dialog_manager.dialog_data.get('admin_open_object_id')

    # Обновляем объект в БД
    new_object_data = {'status': '❌', 'delete_reason': delete_reason}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    # Оповещаем Администратора и отправляем в предыдущие окно
    await dialog_manager.event.answer('Объект отклонён!')
    await dialog_manager.switch_to(AdminDialog.all_objects_moderated)