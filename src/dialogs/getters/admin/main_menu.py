import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from config import Config
from src.database.requests.country import db_get_country, db_update_countries
from src.database.requests.object import db_get_object
from src.database.requests.settings import db_update_info
from src.database.requests.user import db_get_user
from src.dialogs.dialogs_states import AdminDialog
from src.utils.country_updater import get_country_list


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


# Удаляет сообщение спустя время
async def delete_message_delayed(bot, chat_id, message_id, delay):
  await asyncio.sleep(delay)
  await bot.delete_message(chat_id, message_id)


# Обновляет актуальный список стран, основываясь на названиях топиков в чате
async def update_countries(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.event.answer('Ожидайте...')

    # Парсим все топики чата, выводи из них название стран с id топика
    country_list = await get_country_list(Config.chat)

    # Обновляем базу данных
    await db_update_countries(country_list)

    # Формируем информационное сообщение для Администратора
    country_message = '<b>База данных обновлена! Получены новые данные:</b>\n\n'
    country_count = 1
    for country in country_list:
        country_message += f'{country_count}) {country[0]} - topic_id: {country[1]}\n'
        country_count += 1
    country_message += '\n<b>Это сообщение будет автоматически удалено через 10 секунд</b>'

    # Отправляем сервисное уведомление Администратору
    service_message = await dialog_manager.event.bot.send_message(dialog_manager.event.from_user.id, country_message)
    # Удаляем сервисное уведомление через 10 секунд
    asyncio.create_task(
        delete_message_delayed(dialog_manager.event.bot, dialog_manager.event.from_user.id, service_message.message_id,
        delay=10)
    )


# Получаем сообщение, которое будет отправлено в массовой рассылке
async def pre_mass_send_getter(dialog_manager: DialogManager, **kwargs):
    mass_send_text = dialog_manager.find('mass_send_text').get_value()
    return {'mass_send_text': mass_send_text}


# Отдельно от основного потока продолжаем массовую рассылку
async def auto_mass_send(bot, users_list, mass_send_text):
    msg_count = 0

    # рассылаем смс всем пользователям из списка
    for user in users_list:
        telegram_id = user['telegram_id']

        if telegram_id in Config.admin_ids:
            # Админа пропускаем
            continue

        try:
            # Отправляем сообщение Пользователю
            await bot.send_message(telegram_id, mass_send_text)
            msg_count += 1
        except Exception as e:
            print(f'Ошибка при отправке массовой рассылки:\n\n{e}')
        await asyncio.sleep(0.7)

    # Оповещаем о завершении работы
    for admin in Config.admin_ids:
        try:
            # Отправляем сообщение Пользователю
            await bot.send_message(admin, f"📢 <b>Массовая рассылка успешно завершена!</b>\n\n"
                                          f"Отправлено сообщений в количестве: <code>{msg_count}шт.</code>")
        except Exception as e:
            print(f'Ошибка при отправке инфы о завершении массовой рассылки:\n\n{e}')


# Начать массовую рассылку
async def start_mass_send(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    mass_send_text = dialog_manager.find('mass_send_text').get_value()
    users_list = await db_get_user()
    bot = dialog_manager.event.bot

    asyncio.create_task(
        auto_mass_send(bot, users_list, mass_send_text)
    )