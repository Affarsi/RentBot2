from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Counter
from aiogram_dialog.widgets.text import Const

from src.dialogs.dialogs_states import Payment

# Меню для пополнения баланса
payment_main_window = Window(
    Const(
        '<b>Укажите сумму, на которую желаете пополнить баланс:</b>'
    ),

    Counter(
        id='select_amount',
        plus=Const('+100 руб.'),
        minus=Const('-100 руб.'),
        min_value=100,
        increment=100,
        default=100,
    ),
    Button(Const('💰 Начать оплату [комиссия 0%]'), id='make_payment', on_click=...),
    Cancel(Const('Назад'), id='to_start_main_menu_dialog'),

    state=Payment.main
)