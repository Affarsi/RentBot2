from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Button

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin import admin_menu_getter

# Основное меню Администратора
admin_menu_window = Window(
    Format(
        "<b>🖥 Панель администрирования:</b>\n"
        "├Кол-во стран: <code>{all_countries_count}</code>\n"
        "├кол-во объектов: <code>{all_objects_count}</code>\n"
        "└кол-во пользователей: <code>{all_users_count}</code>"
    ),


    Button(Const('🏠 Все объекты'), id='all_objects', on_click=...),
    Button(Const('👥 Все пользователи'), id='all_users', on_click=...),
    Button(Const('🔄 Обновить страны'), id='update_countries', on_click=...),
    Start(Const('🖥 Выйти из панели Администрирования'), id='user_menu', state=UserDialog.main_menu),

    getter=admin_menu_getter,
    state=AdminDialog.menu
)