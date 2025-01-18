import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Button, Group, ScrollingGroup, Select, SwitchTo, Row, Url

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin.all_objects_manager import all_objects_count_getter, all_objects_count_and_sg_list_getter
from src.dialogs.getters.admin.main_menu import admin_menu_getter
from src.dialogs.getters.admin.users_manager import all_users_getter, admin_open_user_account, user_account_getter, \
    new_user_status_input, new_user_obj_limit_input

# Выбор категории объектов, которые Администратор хочет посмотреть
all_objects_manager_window = Window(
    Const("<b>✨ Выберите категорию объектов:</b>"),

    SwitchTo(Format('На модерации - {on_moderation_count} шт.'), id='all_moderation_objects', state=AdminDialog.all_objects_moderated),
    SwitchTo(Format('Опубликованные - {submit_count} шт.'), id='all_submit_objects', state=AdminDialog.all_objects_confirmed),
    SwitchTo(Format('Удалённые - {deleted_count} шт.'), id='all_deleted_objects', state=AdminDialog.all_objects_deleted),
    SwitchTo(Const('Назад'), id='back_to_admin_menu', state=AdminDialog.menu),

    getter=all_objects_count_and_sg_list_getter,
    state=AdminDialog.all_objects_manager
)

# Список объектов со статусом "На модерации"
all_objects_moderated_window = Window(
    Const('<b>✨ Список объектов, находящихся на модерации:</b>'),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='admin_s_moderated_object',
                item_id_getter=operator.itemgetter(1),
                items='moderated_objects_list',
                on_click=...,
            ),
            id='admin_moderated_objects_sg',
            width=2,
            height=7,
        ),
        # поиск по generate_id
        SwitchTo(Const('Назад'), id='back_to_all_objects_manager', state=AdminDialog.all_objects_manager)
    ),

    getter=all_objects_count_and_sg_list_getter,
    state=AdminDialog.all_objects_moderated
)

# Список объектов со статусом "Одобрено"
all_objects_confirmed_window = Window(
    Const('<b>✨ Список успешно опубликованных объектов:</b>'),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='admin_s_confirmed_object',
                item_id_getter=operator.itemgetter(1),
                items='confirmed_objects_list',
                on_click=...,
            ),
            id='admin_confirmed_objects_sg',
            width=2,
            height=7,
        ),
        # поиск по generate_id
        SwitchTo(Const('Назад'), id='back_to_all_objects_manager', state=AdminDialog.all_objects_manager)
    ),

    getter=all_objects_count_and_sg_list_getter,
    state=AdminDialog.all_objects_confirmed
)

# Список объектов со статусом "Удалено"
all_objects_deleted_window = Window(
    Const('<b>✨ Список удалённых объектов:</b>'),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='admin_s_deleted_object',
                item_id_getter=operator.itemgetter(1),
                items='deleted_objects_list',
                on_click=...,
            ),
            id='admin_deleted_objects_sg',
            width=2,
            height=7,
        ),
        # поиск по generate_id
        SwitchTo(Const('Назад'), id='back_to_all_objects_manager', state=AdminDialog.all_objects_manager)
    ),

    getter=all_objects_count_and_sg_list_getter,
    state=AdminDialog.all_objects_deleted
)