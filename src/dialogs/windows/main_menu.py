from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Button

from src.dialogs.dialogs_states import UserDialog
from src.dialogs.getters.user import user_getter

# Основное меню Пользователя
main_menu_window = Window(
    Format(
        "👋 <b>@{username}, Добро пожаловать!</b>\n\n"
        "👤Ваш статус: <code>{status}</code>\n"
        "🏠Создано объектов: <code>{obj_list_len} из {obj_limit}</code>"
    ),

    Group(
        SwitchTo(Const('🏢 Мои объекты'), id='my_objects', state=UserDialog.objects_manager),
        Row(
            SwitchTo(Const('📕 Информация'), id='info', state=UserDialog.info),
            Url(Const('🦸‍♂️ Тех. Поддержка'), Const('https://t.me/sermseo')),
        ),
        Button(Const('🖥 Панель Администрирования'), id='open_admin_panel', when=F['is_admin']),
    ),

    getter=user_getter,
    state=UserDialog.main_menu
)