import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, SwitchTo, Row, Url
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.dialogs_states import AdminDialog
from src.dialogs.getters.admin.users_manager import all_users_getter, admin_open_user_account, user_account_getter, \
    new_user_status_input, new_user_obj_limit_input, search_user_by_username, new_user_plus_balance_input

# Менеджер всех пользователей
users_manager_window = Window(
    Const("<b>✨ Выберите пользователя:</b>\n\n"
          "Или отправьте его @username для автоматического поиска!"),

    MessageInput(search_user_by_username, filter=F.text),

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
        Button(Const('🔍 Отправьте @username для поиска'), id='find_user_by_username', on_click=...),
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
        "├<b>Создано объектов:</b> <code>{obj_list_len}</code>\n"
        "│\n"
        "└<b>Баланс:</b> <code>{balance}руб.</code>"
    ),

    Button(Const('Выберите, что хотели бы изменить:'), id='plug_btn'),
    Row(
        SwitchTo(Const('Статус'), id='change_user_status', state=AdminDialog.change_user_status),
        SwitchTo(Const('Лимит объектов'), id='change_user_obj_limit', state=AdminDialog.change_user_obj_limit),
        SwitchTo(Const('Баланс'), id='change_user_balance', state=AdminDialog.change_user_balance),
    ),
    Url(Const('📞 Связаться с Пользователем'), Format('https://t.me/{username}')),
    SwitchTo(Const('Назад'), id='back_to_users_manager', state=AdminDialog.users_manager),

    getter=user_account_getter,
    state=AdminDialog.open_user_account
)

# Окно изменения статуса Пользователя
change_user_status_window = Window(
    Const('<b>Отправьте новый статус, который будет присвоен Пользователю:</b>'),

    MessageInput(new_user_status_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_open_user_acc', state=AdminDialog.open_user_account),

    state=AdminDialog.change_user_status
)

# Окно изменения лимита объектов Пользователя
change_user_obj_limit_window = Window(
    Const('<b>Отправьте новый лимит объектов, который будет прикреплен к Пользователю:</b>'),

    MessageInput(new_user_obj_limit_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_open_user_acc', state=AdminDialog.open_user_account),

    state=AdminDialog.change_user_obj_limit
)

# Окно изменения баланса Пользователя
change_user_balance_window = Window(
    Const(
        '<b>Отправьте число на которое будет <i>ПРИПЛЮСОВАН</i> баланс:</b>\n\n'
        '⚠️ Данная функция <b>ПРИБАВЛЯЕТ</b> баланс Пользователю, а не изменяет его на тот, который вы укажите\n\n'
        '<b>Например:</b>\n'
        'У Пользователя <code>500 руб.</code> на балансе\n'
        'Если вы сейчас отправите число <code>500</code>, то у Пользователя баланс станет: <code>1000 руб.</code>\n'
        'Вы <b>ПРИПЛЮСУЕТЕ</b> ему <code>500</code> рублей к балансу!\n\n'
        '<b>Чтобы уменьшить баланс, отправьте <code>-500</code></b>'
    ),

    MessageInput(new_user_plus_balance_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_open_user_acc', state=AdminDialog.open_user_account),

    state=AdminDialog.change_user_balance
)