from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, Button, SwitchTo

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin.main_menu import admin_menu_getter

# Основное меню Администратора
admin_menu_window = Window(
    Format(
        "<b>🖥 Панель администрирования:</b>\n"
        "├Кол-во стран: <code>{all_countries_count}</code>\n"
        "├кол-во объектов: <code>{all_objects_count}</code>\n"
        "└кол-во пользователей: <code>{all_users_count}</code>"
    ),


    SwitchTo(Const('🏠 Все объекты'), id='all_objects', on_click=...),
    SwitchTo(Const('👥 Все пользователи'), id='all_users', state=AdminDialog.users_manager),
    Button(Const('🔄 Обновить страны'), id='update_countries', on_click=...),
    Start(Const('🖥 Выйти из панели Администрирования'), id='user_menu', state=UserDialog.main_menu),

    getter=admin_menu_getter,
    state=AdminDialog.menu
)