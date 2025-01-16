from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, Button

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin.admin import admin_menu_getter

# Менеджер всех пользователей
users_manager_window = Window(
    Const("<b>Выберите пользователя:</b>"),

    Button(Const('🏠 Все объекты'), id='all_objects', on_click=...),
    Button(Const('👥 Все пользователи'), id='all_users', on_click=...),
    Button(Const('🔄 Обновить страны'), id='update_countries', on_click=...),
    Start(Const('🖥 Выйти из панели Администрирования'), id='user_menu', state=UserDialog.main_menu),

    getter=all_users_getter,
    state=AdminDialog.users_manager
)