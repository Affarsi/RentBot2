from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Button

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.main_menu import user_main_getter, info_getter

# Основное меню Пользователя
main_menu_window = Window(
    Format(
        "👋 <b>@{username}, Добро пожаловать!</b>\n\n"
        "👤Ваш статус: <code>{status}</code>\n"
        "🏠Создано объектов: <code>{obj_list_len} из {obj_limit}</code>"
    ),

    Group(
        SwitchTo(Const('🏢 Мои объекты'), id='my_objects', state=UserDialog.my_objects_manager),
        Row(
            SwitchTo(Const('📕 Информация'), id='info', state=UserDialog.info),
            Url(Const('🦸‍♂️ Тех. Поддержка'), Const('https://t.me/sermseo')),
        ),
        Start(Const('🖥 Панель Администрирования'), id='admin_menu', state=AdminDialog.menu, when=F['is_admin']),
    ),

    getter=user_main_getter,
    state=UserDialog.main_menu
)

# Основное меню Пользователя
info_window = Window(
    Format('{info}'),

    SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

    getter=info_getter,
    state=UserDialog.info
)