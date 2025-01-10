import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select

from src.dialogs.dialogs_states import User
from src.dialogs.getters.object import my_objects_getter
from src.dialogs.getters.user import user_getter

# Основное меню Пользователя
objects_manager_window = Window(
    Const(
        '''<b>Добро пожаловать в раздел Мои объекты</b>
        
        Вы можете выбрать уже созданный объект:
        ✅ - объект опубликован
        🔄 - объект на модерации    
        ❌ - объект удалён
        
        А также отредактировать уже опубликованный объект или создать новый, используя меню ниже'''
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
        SwitchTo(Const('➕ Создать объект'), id='my_objects', state=User.objects_manager),
        SwitchTo(Const('Назад'), id='to_main_menu', state=User.main_menu),
    ),

    getter=my_objects_getter,
    state=User.objects_manager
)