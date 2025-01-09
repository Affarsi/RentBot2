from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.dialogs_states import User

from src.database.requests.user import db_new_user

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE) # Принимает только личные сообщения


# /start от Пользователя
@router.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    # Получение данных о Пользователе
    full_mane = message.from_user.full_name or "NotFullName"
    username = message.from_user.username or "NotUsername"
    telegram_id = message.from_user.id

    # Добавление пользователя в БД
    await db_new_user(
        telegram_id=telegram_id,
        full_name=full_mane,
        username=username,
    )

    # Запускаем диалоговое окно
    await dialog_manager.start(User.main_menu, mode=StartMode.RESET_STACK)



# /start от Администратора


