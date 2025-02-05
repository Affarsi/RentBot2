import datetime

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCounter
from aiogram.types import CallbackQuery

from config import Config
from src.database.requests.payment import db_new_payment, db_update_payment_success
from src.database.requests.user import db_update_user
from src.dialogs.dialogs_states import Payment
from src.payments.tinkoff.payment_manager import create_payment_link, check_payment


# Запоминание выбранной суммы
async def get_amount(
        callback: CallbackQuery,
        widget: ManagedCounter,
        dialog_manager: DialogManager,
):
    amount = widget.get_value()
    dialog_manager.dialog_data['payment_amount'] = amount


# Формирование платежа Тинькофф
async def create_payment(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Инициализация данных
    amount = dialog_manager.dialog_data.get('payment_amount', Config.price_amount)
    telegram_id = callback.from_user.id
    generate_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Создание ссылки для оплаты
    order_id = f'{telegram_id}-n{generate_id}'
    dialog_manager.dialog_data['order_id'] = order_id
    payment_link = await create_payment_link(amount, order_id)

    # Проверка и сохранение ссылки
    if not payment_link:
        await callback.answer('Ошибка при создании оплаты!')
        return
    else:
        dialog_manager.dialog_data['payment_url'] = payment_link

    # Сохранение в БД
    await db_new_payment(telegram_id, order_id, amount)

    # Переход к следующему шагу
    await dialog_manager.switch_to(state=Payment.waiting_payment)


# Передает в окно Пользователя ссылку на оплату
async def payment_link_getter(dialog_manager: DialogManager, **kwargs):
    url = dialog_manager.dialog_data.get('payment_url')
    return {'payment_link': url}


# Проверяет платеж
async def check_payment_btn(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Получаем информацию о платеже
    order_id = dialog_manager.dialog_data.get('order_id')
    payment_data = await check_payment(order_id)
    # {'Success': True, 'ErrorCode': '0', 'Message': 'OK', 'TerminalKey': '1737740259529DEMO', 'OrderId': '902966420-n11667',
    # 'Payments': [{'Success': True, 'Amount': 30000, 'Status': 'CONFIRMED', 'PaymentId': '5752628003'}]}

    # Если оплата прошла
    is_status = payment_data.get('Payments')[0].get('Status')
    if is_status == 'CONFIRMED':
        await callback.answer('Оплата прошла успешно!')

        # Изменяем данные в БД
        amount = payment_data.get('Payments')[0].get('Amount') / 100 # потому что в копейках
        await db_update_user(telegram_id=callback.from_user.id, plus_balance=amount)
        await db_update_payment_success(order_id=order_id)

        # Перебрасываем Пользователя в главное меню
        await dialog_manager.done()

    # Если оплата не прошла
    else:
        await callback.answer('Оплата еще не обнаружена')