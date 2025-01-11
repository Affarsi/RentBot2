import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select, Button

from src.dialogs.dialogs_states import UserDialog, CreateObject
from src.dialogs.getters.object import my_objects_getter, start_create_object, open_my_object, delete_my_object
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
    Const('<b>Выше вы видите ваш пост, который успешно прошёл модерацию и был опубликован в нашем канале</b>\n\n'
        'Вы можете: Внести корректировки или Удалить его\n\n'
        '<b>После редактирования</b> - пост снова попадёт на модерацию, также вы не сможете загрузить больше фотографий, '
        'чем на данный момент содержит пост!\n'
        '<b>После удаления</b> - пост не будет подлежать восстановлению!'),

        SwitchTo(Const('✏️ Редактировать объект'), id='to_main_menu', state=UserDialog.main_menu),
        Button(Const('❌ Удалить объект'), id='dell_my_object', on_click=delete_my_object),
        SwitchTo(Const('Назад'), id='to_main_menu', state=UserDialog.main_menu),

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