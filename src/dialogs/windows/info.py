from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, Cancel

from src.dialogs.dialogs_states import UserDialog
from src.dialogs.getters.info import info_getter
from src.dialogs.getters.user import user_getter

# Основное меню Пользователя
info_window = Window(
    Format('{info}'),

    SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

    getter=info_getter,
    state=UserDialog.info
)