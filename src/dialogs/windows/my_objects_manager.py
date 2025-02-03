import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Row, SwitchTo, ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.dialogs_states import UserDialog
from src.dialogs.getters.edit_object import start_edit_menu_dialog
from src.dialogs.getters.my_objects_manager import my_objects_getter, start_create_object, open_my_object, \
    delete_my_object, \
    object_confirmed_getter, invert_edit_menu_open, invert_delete_object_confirm_menu, my_object_delete_getter, \
    restore_object

# Меню редактирование объекта
object_edit_menu = Group(
    Button(Const('✏️ Меню редактирования'), id='invert_edit_menu_my_object', on_click=invert_edit_menu_open),
    Row(
        Button(Const('Цена и Условия'), id='edit_conditions', on_click=start_edit_menu_dialog),
        Button(Const('Описание'), id='edit_description', on_click=start_edit_menu_dialog),

        when=F['edit_menu_open']
    ),
    Row(
        Button(Const('Контакты'), id='edit_contacts', on_click=start_edit_menu_dialog),
        Button(Const('Фотографии'), id='edit_photos', on_click=start_edit_menu_dialog),

            when=F['edit_menu_open']
    ),
)


# Раздел 'Мои объекты'
my_objects_manager_window = Window(
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
        Button(Format('{create_object_btn_text}'), id='create_object', on_click=start_create_object), # Создание объекта
        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),
    ),

    getter=my_objects_getter,
    state=UserDialog.my_objects_manager
)

# Просмотр объекта, находящегося в статусе 'Принят'
my_object_confirmed_window = Window(
    Format('<b>✨Выберите действие:</b>\n\n🗓 До конца размещения объекта: <code>{days_left}</code>'),

    Group(
        object_edit_menu, # Меню редактирование объекта
        Button(Const('❌ Удалить объект'), id='invert_delete_object_confirm_menu',
               on_click=invert_delete_object_confirm_menu),
        Row(
            Button(Const('🚨ПОДТВЕРДИТЬ УДАЛЕНИЕ ОБЪЕКТА🚨'), id='dell_my_object', on_click=delete_my_object),

            when=F['delete_object_confirm_menu']
        ),
        SwitchTo(Const('Назад'), id='back_to_my_objects_manager', state=UserDialog.my_objects_manager),
    ),

    getter=object_confirmed_getter,
    state=UserDialog.my_open_object_confirmed
)

# Просмотр объекта, находящегося в статусе 'На модерации'
my_object_moderated_window = Window(
    Const('<b>Выше вы видите ваш пост, но он ещё находится в процессе модерации!\n\n'
          'Если ваш пост находится на модерации больше 48 часов или вы желаете его удалить - '
          'напишите в Тех. Поддержку!\n'
          'Спасибо за понимание!</b>'),

    SwitchTo(Const('Назад'), id='back_to_my_objects_manager', state=UserDialog.my_objects_manager),

    state=UserDialog.my_open_object_moderated
)

# Просмотр объекта, находящегося в статусе 'Удалён'
my_object_deleted_window = Window(
    Format('<b>Объект удалён</b>\n\n'
           '<blockquote><b>Причина:</b>\n'
           '{delete_reason}</blockquote>'),

    Group(
    object_edit_menu,  # Меню редактирование объекта
    Button(Format('{edit_object_btn_text}'), id='restore_obj', on_click=restore_object), # Восстановление объекта
    SwitchTo(Const('Назад'), id='back_to_my_objects_manager', state=UserDialog.my_objects_manager),
    ),

    getter=my_object_delete_getter,
    state=UserDialog.my_open_object_deleted
)

