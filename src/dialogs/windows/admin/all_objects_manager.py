import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, SwitchTo, Row

from src.dialogs.dialogs_states import AdminDialog
from src.dialogs.getters.admin.all_objects_manager import all_objects_count_and_sg_list_getter, admin_open_object, \
    invert_admin_edit_menu_open, invert_admin_dell_obj_confirm_menu, admin_delete_object, accept_moderated_object, \
    reason_object_reject_input, reason_object_delete_input, \
    admin_object_delete_reason_getter, admin_open_object_confirmed_getter, admin_restore_object
from src.dialogs.getters.admin.edit_object import start_admin_edit_menu_dialog

admin_object_edit_menu = Group(
    Button(Const('✏️ Меню редактирования'), id='invert_admin_edit_menu_object', on_click=invert_admin_edit_menu_open),
    Row(
        Button(Const('Цена и Условия'), id='admin_edit_conditions', on_click=start_admin_edit_menu_dialog),
        Button(Const('Описание'), id='admin_edit_description', on_click=start_admin_edit_menu_dialog),
        Button(Const('Контакты'), id='admin_edit_contacts', on_click=start_admin_edit_menu_dialog),
        Button(Const('Фотографии'), id='admin_edit_photos', on_click=start_admin_edit_menu_dialog),

        when=F['admin_dit_menu_open']
    ),
)


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
                on_click=admin_open_object,
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
                on_click=admin_open_object,
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
                on_click=admin_open_object,
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

# Просмотр объекта со статусом "На модерации"
admin_open_object_moderated_window = Window(
    Const('<b>Объект на модерации</b>'),

    admin_object_edit_menu, # Меню редактирования объекта
    Row(
        SwitchTo(Const('❌ Отклонить'), id='reject_moderated_object', state=AdminDialog.enter_object_reject_reason),
        Button(Const('✅ Одобрить'), id='accept_moderated_object', on_click=accept_moderated_object),
    ),
    SwitchTo(Const('Назад'), id='back_to_all_deleted_objects', state=AdminDialog.all_objects_moderated),

    getter=admin_open_object_confirmed_getter,
    state=AdminDialog.admin_open_object_moderated
)

# Просмотр объекта со статусом "Одобрено"
admin_open_object_confirmed_window = Window(
    Format(
        '<b>Объект был одобрен!</b>\n\n'
        '👤 <b>{full_name}</b>: @{username}\n'
        '<b>Статус:</b> <code>{status}</code>\n'
        '<b>Создано объектов:</b> <code>{obj_list_len}</code>\n'
        '<b>Лимит объектов:</b> <code>{obj_limit}</code>\n\n'
        '🗓 До конца размещения объекта: <code>{days_left}</code>'
    ),

    admin_object_edit_menu, # Меню редактирования объекта
    Button(Const('❌ Удалить объект'), id='admin_invert_delete_object_confirm_menu', on_click=invert_admin_dell_obj_confirm_menu),
    Row(
        SwitchTo(Const('🚨ПОДТВЕРДИТЬ УДАЛЕНИЕ ОБЪЕКТА🚨'), id='admin_delete_object', state=AdminDialog.enter_object_delete_reason),

        when=F['admin_delete_object_confirm_menu']
    ),
    SwitchTo(Const('Назад'), id='back_to_all_deleted_objects', state=AdminDialog.all_objects_confirmed),

    getter=admin_open_object_confirmed_getter,
    state=AdminDialog.admin_open_object_confirmed
)


# Просмотр объекта со статусом "Удалено"
admin_open_object_deleted_window = Window(
    Format('<b>Объект удалён\n\nПричина:</b>\n{delete_reason}'),

    admin_object_edit_menu, # Меню редактирования объекта
    Button(Format('🔄 Восстановить и одобрить объект'), id='admin_restore_obj', on_click=admin_restore_object),
    SwitchTo(Const('Назад'), id='back_to_all_deleted_objects', state=AdminDialog.all_objects_deleted),

    getter=admin_object_delete_reason_getter,
    state=AdminDialog.admin_open_object_deleted
)


# Ввести причину отклонения объекта, находящегося на модерации
object_reject_reason_window = Window(
    Const('<b>Вы собираетесь удалить объект!\n\nРаспишите ОБЪЕКТИВНО и ПОДРОБНО причину удаления:</b>'),

    MessageInput(reason_object_reject_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_open_object_moderated', state=AdminDialog.admin_open_object_moderated),

    state=AdminDialog.enter_object_reject_reason
)


# Ввести причину удаления уже опубликованного объекта
object_delete_reason_window = Window(
    Const('<b>Вы собираетесь удалить объект!\n\nРаспишите ОБЪЕКТИВНО и ПОДРОБНО причину удаления:</b>'),

    MessageInput(reason_object_delete_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_open_object_confirmed', state=AdminDialog.admin_open_object_confirmed),

    state=AdminDialog.enter_object_delete_reason
)