from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.dialogs_states import UserPanel
from src.database.requests.user import db_new_user

bot_handler = Router()
bot_handler.message.filter(F.chat.type == ChatType.PRIVATE) # Принимает только личные сообщения


# /start от Пользователя
@bot_handler.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    # Получаем данные о Пользователе
    full_mane = message.from_user.full_name or "NotFullName"
    username = message.from_user.username or "NotUsername"

    # Добавляем пользователя в БД
    await db_new_user(
        telegram_id=message.from_user.id,
        full_name=full_mane,
        username=username,
        invite_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Запускаем диалоговое окно
    await dialog_manager.start(UserPanel.main_menu, mode=StartMode.RESET_STACK)



# /start от Администратора


