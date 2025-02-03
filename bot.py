import pytz
import asyncio
from config import Config

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.database.run_db import create_db
from src.handlers.commands import router as commands_router
from src.dialogs.dialogs_manager import user_dialog, create_object_dialog, edit_object_dialog, admin_dialog, \
    admin_edit_object_dialog, payment_dialog
from src.utils.objects_monitoring_sistem import objects_monitoring

bot = Bot(Config.bot_token, default=DefaultBotProperties(parse_mode='HTML')) # Создание aiogram бота
scheduler = AsyncIOScheduler() # Создание асинхронного планировщика


# Запуск систему мониторинга объектов
async def scheduler_start():
    print('scheduler запущен!')
    scheduler.add_job(objects_monitoring, IntervalTrigger(hours=12), args=[bot])
    scheduler.start()


# Запуск aiogram бота
async def aiogram_run():
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_routers(
        user_dialog,
        create_object_dialog,
        edit_object_dialog,

        admin_dialog,
        admin_edit_object_dialog,

        payment_dialog,

        commands_router
    )

    setup_dialogs(dp)

    print('Бот запущен!')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    # Запуск базы данных
    await create_db()

    # Установка часового пояса
    pytz.timezone('Europe/Moscow')

    task1 = asyncio.create_task(scheduler_start())
    task2 = asyncio.create_task(aiogram_run())
    await asyncio.gather(task1, task2)



if __name__ == '__main__':
    asyncio.run(main())