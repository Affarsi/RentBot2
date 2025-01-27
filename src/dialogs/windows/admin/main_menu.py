from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, Button, SwitchTo, Row, Group

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin.main_menu import admin_menu_getter, take_new_info_input, update_countries
from src.dialogs.getters.main_menu import info_text_getter

# Основное меню Администратора
admin_menu_window = Window(
    Format(
        "<b>🖥 Панель администрирования:</b>\n"
        "├Кол-во стран: <code>{all_countries_count}</code>\n"
        "├Кол-во объектов: <code>{all_objects_count}</code>\n"
        "└Кол-во пользователей: <code>{all_users_count}</code>"
    ),

    Group(
        Row(
            SwitchTo(Const('🏠 Все объекты'), id='all_objects', state=AdminDialog.all_objects_manager),
            SwitchTo(Const('👥 Все пользователи'), id='all_users', state=AdminDialog.users_manager),
        ),
        Button(Const('Обновить страны'), id='update_countries', on_click=update_countries),
        SwitchTo(Const('Изменить "Информация"'), id='update_info', state=AdminDialog.update_info),
        Start(Const('👨 Вернуться в панель Пользователя'), id='user_menu', state=UserDialog.main_menu),
    ),

    getter=admin_menu_getter,
    state=AdminDialog.menu
)

# Изменить информацию в разделе FAQ
update_info_window = Window(
    Format('<b>Старое описание раздела "Информация":</b>\n\n{info_text}\n\n<b>Отправьте новое описание:</b>'),

    MessageInput(take_new_info_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_menu', state=AdminDialog.menu),

    getter=info_text_getter,
    state=AdminDialog.update_info
)