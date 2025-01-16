from config import Config

from aiogram_dialog import DialogManager

from src.database.requests.settings import db_get_info
from src.database.requests.user import db_get_user


# Возвращает всю информацию о Пользователе
async def user_main_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.event.from_user.id
    user_dict = await db_get_user(telegram_id=telegram_id)

    # Проверяем, является ли пользователь администратором
    is_admin = telegram_id in Config.admin_ids
    user_dict['is_admin'] = is_admin

    return user_dict


# Возвращает текст для раздела Информация
async def info_getter(**kwargs):
    res = {'info': await db_get_info()}
    return res