from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Counter, Url, WebApp
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.dialogs_states import Payment
from src.dialogs.getters.payment import create_payment, get_amount, payment_link_getter, check_payment_btn

# Меню для пополнения баланса
payment_main_window = Window(
    Const(
        '<b>Укажите сумму, на которую желаете пополнить баланс:</b>'
    ),

    Counter(
        id='select_amount',
        plus=Const('+50'),
        minus=Const('-50'),
        min_value=50,
        increment=50,
        default=100,
        on_value_changed=get_amount
    ),
    Button(Const('💰 Начать оплату [Тинькофф - комиссия 0%]'), id='make_payment', on_click=create_payment),
    Cancel(Const('Назад'), id='to_start_main_menu_dialog'),

    state=Payment.main
)

# Ожидание оплаты
waiting_payment_window = Window(
    Const(
        '<b>Для оплаты перейдите по ссылке</b>\n\n'
        'После успешной оплаты нажмите кнопку "Проверить платеж"!'
    ),

    WebApp(Const('💳 Перейти к оплате'), Format('{payment_link}'), id='payment_link'),
    Button(Const('⏳ Проверить платёж'), id='check_payment', on_click=check_payment_btn),
    Cancel(Const('Отменить оплату'), id='to_start_main_menu_dialog'),

    getter=payment_link_getter,
    state=Payment.waiting_payment
)