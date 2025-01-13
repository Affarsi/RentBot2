import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select, Button

from src.dialogs.dialogs_states import UserDialog, CreateObject
from src.dialogs.getters.object import my_objects_getter, start_create_object, open_my_object, delete_my_object, \
    object_confirmed_getter, invert_edit_menu_open, invert_delete_object_confirm_menu
from src.dialogs.getters.user import user_getter

# Раздел 'Мои объекты'
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
                on_click=open_my_object,
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

# Просмотр объекта, находящегося в статусе 'Принят'
object_confirmed_window = Window(
    Const('<b>✨Выберите действие:</b>'),

        Button(Const('✏️ Меню редактирования'), id='invert_edit_menu_my_object', on_click=invert_edit_menu_open),
        Row(
            Button(Const('Адрес'), id='dell_my_object', on_click=delete_my_object),
            Button(Const('Цена и Условия'), id='dell_my_object', on_click=delete_my_object),
            Button(Const('Описание'), id='dell_my_object', on_click=delete_my_object),
            Button(Const('Фотографии'), id='dell_my_object', on_click=delete_my_object),

            when=F['edit_menu_open']
        ),
        Button(
            Const('❌ Удалить объект'),
            id='invert_delete_object_confirm_menu',
            on_click=invert_delete_object_confirm_menu
        ),
        Row(
            Button(Const('🚨ПОДТВЕРДИТЬ УДАЛЕНИЕ ОБЪЕКТА🚨'), id='dell_my_object', on_click=delete_my_object),

            when=F['delete_object_confirm_menu']
        ),
        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

    getter=object_confirmed_getter,
    state=UserDialog.open_my_object_confirmed
)

# Просмотр объекта, находящегося в статусе 'На модерации'
object_moderated_window = Window(
    Const('<b>Выше вы видите ваш пост, но он ещё находится в процессе модерации!\n\n'
          'Если ваш пост находится на модерации больше 48 часов или вы желаете его удалить - '
          'напишите в Тех. Поддержку!\n'
          'Спасибо за понимание!</b>'),

        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

    state=UserDialog.open_my_object_moderated
)

# Просмотр объекта, находящегося в статусе 'Удалён'
object_deleted_window = Window(
    Const('<b>К сожалению, ваш пост был удалён администратором.\n\n'
          'Причина удаления:\n'
          '\n\n'
          'Если вы не согласны с решением администратора - обратитесь в Тех. Поддержку.</b>'),

        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

    state=UserDialog.open_my_object_deleted
)