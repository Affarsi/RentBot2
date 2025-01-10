from aiogram_dialog import DialogManager

from src.database.requests.user import db_get_user


# Возвращает всю информацию о Пользователе
async def user_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.event.from_user.id
    user_dict = await db_get_user(telegram_id=telegram_id)
    return user_dict