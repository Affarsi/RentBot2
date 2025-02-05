import asyncio

from config import Config
from aiogram_dialog import DialogManager

from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button

from src.database.requests.settings import db_get_info
from src.database.requests.user import db_get_user, db_update_user


# Возвращает всю информацию о Пользователе
async def user_main_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.event.from_user.id
    user_dict = await db_get_user(telegram_id=telegram_id)

    # Проверяем, является ли пользователь администратором
    is_admin = telegram_id in Config.admin_ids
    user_dict['is_admin'] = is_admin

    # Состояние автопродления
    if user_dict.get('recurring_payments'):
        user_dict['recurring_payments_btn_text'] = 'Автопродление объектов [Вкл]'
    else:
        user_dict['recurring_payments_btn_text'] = 'Автопродление объектов [Выкл]'

    return user_dict


# Возвращает текст для раздела Информация
async def info_text_getter(**kwargs):
    res = {'info_text': await db_get_info()}
    return res


# Состояние рекуррентных платежей изменено
async def recurring_payments_changed(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Инициализация данных
    tg_id = callback.from_user.id
    user_dict = await db_get_user(telegram_id=tg_id)

    # Проверяем, существует ли ключ и получаем текущее значение
    recurring_payments = user_dict.get('recurring_payments')

    # Изменяем данные в БД
    new_recurring_payments = not recurring_payments
    await db_update_user(telegram_id=tg_id, recurring_payments=new_recurring_payments)

    # Оповещаем Пользователя
    if new_recurring_payments:
        await callback.answer('Автопродление включено!')
    else:
        await callback.answer('Автопродление выключено!')