from config import Config

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from src.database.requests.country import db_get_country
from src.database.requests.object import db_get_object
from src.database.requests.settings import db_update_info
from src.database.requests.user import db_get_user
from src.dialogs.dialogs_states import AdminDialog


# getter для admin_menu, возвращает общую статистику всего бота
async def admin_menu_getter(dialog_manager: DialogManager, **kwargs):
    user_list = await db_get_user()
    object_list = await db_get_object()
    country_list = await db_get_country()

    return {
        'all_countries_count': len(country_list),
        'all_objects_count': len(object_list),
        'all_users_count': len(user_list),
    }


# Изменяет текст в разделе "Информация"
async def take_new_info_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    info_text = message.html_text
    await db_update_info(new_info=info_text)

    await dialog_manager.event.answer('Информация изменена!')
    await dialog_manager.switch_to(AdminDialog.menu)