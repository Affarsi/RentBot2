from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Command

from aiogram_dialog import DialogManager, StartMode

from config import Config
from src.dialogs.dialogs_states import UserPanel

chat_handler = Router()
chat_handler.message.filter(F.chat.type == ChatType.SUPERGROUP) # реагирует только на сообщения из чата


