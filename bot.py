import pytz
import asyncio
from config import Config
from src.database.run_db import create_db

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.handlers.chat_commands import chat_handler as chat_cmd_router
from src.handlers.bot_commands import bot_handler as bot_cmd_router
from src.dialogs.dialogs_manager import user_panel_dialog

bot = Bot(Config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def aiogram_run():
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_routers(
        user_panel_dialog,

        bot_cmd_router,
        chat_cmd_router
    )

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    # Запуск базы данных
    await create_db()

    # Установка часового пояса
    pytz.timezone('Europe/Moscow')

    # Запуск aiogram бота
    print('Бот запущен!')
    await aiogram_run()



if __name__ == '__main__':
    asyncio.run(main())