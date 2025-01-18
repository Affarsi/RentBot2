import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Button, Group, ScrollingGroup, Select, SwitchTo, Row, Url

from src.dialogs.dialogs_states import UserDialog, AdminDialog
from src.dialogs.getters.admin.main_menu import admin_menu_getter
from src.dialogs.getters.admin.users_manager import all_users_getter, admin_open_user_account, user_account_getter, \
    new_user_status_input, new_user_obj_limit_input

# Менеджер всех пользователей
users_manager_window = Window(
    Const("<b>✨ Выберите пользователя:</b>"),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='admin_s_user',
                item_id_getter=operator.itemgetter(1),
                items='all_users_list',
                on_click=admin_open_user_account,
            ),
            id='admin_s_check_user',
            width=2,
            height=7,
        ),
        # поиск по @login
        SwitchTo(Const('Назад'), id='back_to_admin_menu', state=AdminDialog.menu)
    ),

    getter=all_users_getter,
    state=AdminDialog.users_manager
)

# Открытая информация об аккаунте выбранного Пользователя с edit меню
open_user_account_window = Window(
    Format(
        "<b>👤Информация о Пользователе: </b><code>{full_name}</code>\n"
        "│\n"
        "├<b>ID:</b> <code>{telegram_id}</code>\n"
        "├<b>Username:</b> <code>@{username}</code>\n"
        "│\n"
        "├<b>Status:</b> <code>{status}</code>\n"
        "├<b>Лимит объектов:</b> <code>{obj_limit}</code>\n"
        "│\n"
        "└<b>Создано объектов:</b> <code>{obj_list_len}</code>"
    ),

    Row(
        SwitchTo(Const('Изменить статус'), id='change_user_status', state=AdminDialog.change_user_status),
        SwitchTo(Const('Изменить лимит объектов'), id='change_user_obj_limit', state=AdminDialog.change_user_obj_limit),
    ),
    Url(Const('📞 Связаться с Пользователем'), Format('https://t.me/{username}')),
    SwitchTo(Const('Назад'), id='back_to_users_manager', state=AdminDialog.users_manager),

    getter=user_account_getter,
    state=AdminDialog.open_user_account
)

# Окно изменения статуса Пользователя
change_user_status_window = Window(
    Const('Отправьте новый статус, который будет присвоен Пользователю:'),

    MessageInput(new_user_status_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_open_user_acc', state=AdminDialog.open_user_account),

    state=AdminDialog.change_user_status
)

# Окно изменения лимита объектов Пользователя
change_user_obj_limit_window = Window(
    Const('Отправьте новый лимит объектов, который будет прикреплен к Пользователю:'),

    MessageInput(new_user_obj_limit_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_open_user_acc', state=AdminDialog.open_user_account),

    state=AdminDialog.change_user_obj_limit
)