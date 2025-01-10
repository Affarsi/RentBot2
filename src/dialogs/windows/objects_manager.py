import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select, Button

from src.dialogs.dialogs_states import UserDialog, CreateObject
from src.dialogs.getters.object import my_objects_getter, start_create_object
from src.dialogs.getters.user import user_getter

# Основное меню Пользователя
objects_manager_window = Window(
    Const(
        '<b>Добро пожаловать в раздел Мои объекты</b>\n\n'
        'Вы можете открыть уже существующий объект и отредактировать его,'
        'а также создать новый объект, используя меню ниже:\n\n'
        '<blockquote>✅ - объект опубликован\n'
        '🔄 - объект на модерации\n'
        '❌ - объект удалён</blockquote>'
    ),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='s_my_object',
                item_id_getter=operator.itemgetter(1),
                items='my_object_list',
                on_click=...,
            ),
            id='s_my_objects',
            width=2,
            height=7,
        ),
        Button(Const('➕ Создать объект'), id='create_object', on_click=start_create_object),
        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),
    ),

    getter=my_objects_getter,
    state=UserDialog.objects_manager
)