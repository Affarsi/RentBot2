from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.dialogs_states import UserDialog, AdminDialog, Payment
from src.dialogs.getters.main_menu import user_main_getter, info_text_getter, recurring_payments_changed

# Основное меню Пользователя
main_menu_window = Window(
    Format(
        '👋 <b>@{username}, Добро пожаловать!</b>\n\n'
        '👤 Ваш статус: <code>{status}</code>\n'
        '🏠 Ваши лимиты:\n'
        '● Бесплатных объектов: <code>{free_objects_limit} шт.</code>\n'
        '● Платных объектов: <code>{paid_objects_limit} шт.</code>\n\n'
        '💳 Баланс: <code>{balance} руб.</code>\n'
        '🏘 Всего объектов: <code>{obj_list_len} шт.</code>'
    ),

    Group(
        SwitchTo(Const('🏢 Мои объекты'), id='my_objects', state=UserDialog.my_objects_manager),
        Row(
            SwitchTo(Const('📕 Информация'), id='info', state=UserDialog.info),
            Url(Const('🦸‍♂️ Тех. Поддержка'), Const('https://t.me/sermseo')),
        ),
        Start(Const('💳 Пополнить баланс'), id='upgrade_obj_limit', state=Payment.main),
        Button(Format('{recurring_payments_btn_text}'), id='checkbox_recurring_payments', on_click=recurring_payments_changed),
        Start(Const('🖥 Войти в панель Администрирования'), id='admin_menu', state=AdminDialog.menu, when=F['is_admin']),
    ),

    getter=user_main_getter,
    state=UserDialog.main_menu
)

# Основное меню Пользователя
info_window = Window(
    Format('{info_text}'),

    Back(Const('Назад')),

    getter=info_text_getter,
    state=UserDialog.info
)