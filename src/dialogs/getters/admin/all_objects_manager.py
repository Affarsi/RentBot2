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


# Возвращает список всех объектов по типам
