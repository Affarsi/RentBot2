from aiogram_dialog import DialogManager
from aiogram.types import Message

from src.database.requests.user import db_get_user


# Достаёт информацию о пользователе
async def profile_info(dialog_manager: DialogManager, **kwargs) -> dict:
    telegram_id = dialog_manager.event.from_user.id

    # Получаем информацию о Пользователе из БД
    user_dict = await db_get_user(telegram_id=telegram_id)

    # Формируем словарь для диалога
    getter_dict = {
        "user_username": user_dict["username"],
        "user_invite_date": user_dict["invite_date"],
        "user_points": user_dict["points_balance"],
        "user_referrals": user_dict["referrals_count"]
    }

    return getter_dict