import pytz
import asyncio

from config import Config

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.database.run_db import create_db

from src.handlers.commands import router as commands_router

from src.dialogs.dialogs_manager import user_dialog, create_object_dialog, edit_object_dialog, admin_dialog, \
    admin_edit_object_dialog

bot = Bot(Config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def aiogram_run():
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_routers(
        user_dialog,
        create_object_dialog,
        edit_object_dialog,

        admin_dialog,
        admin_edit_object_dialog,

        commands_router
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