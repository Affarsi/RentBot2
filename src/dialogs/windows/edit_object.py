import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select, Button

from src.dialogs.dialogs_states import UserDialog, CreateObject, EditObject
from src.dialogs.getters.edit_object import edit_object_address_input, edit_object_conditions_input, \
    edit_object_description_input
from src.dialogs.getters.object import my_objects_getter, start_create_object, open_my_object, delete_my_object, \
    object_confirmed_getter, invert_edit_menu_open, invert_delete_object_confirm_menu
from src.dialogs.getters.user import user_getter


# Итоговый вариант редактирование с edit_menu
result_and_edit_menu_window = Window(
    Const('<b>Выше вы видите отредактированный пост!\n</b>'
          '<b>Вы можете отказаться от изменений или отправить его на модерацию\n\n</b>'),

    # Button(Const('✅ Отправить на модерацию'), id='submit_edit_object', on_click=submit_edit_object),
    # Cancel(Const('Отменить изменение объекта'), id='stop_edit_object', on_click=clear_dialog_data_edit_object),

    state=EditObject.result_and_edit_menu
)

# Окно для редактирования адреса объекта
edit_address_window = Window(
    Const('<b>Укажите Новый Адрес объекта:</b>\n\n'
          '<i>Например: г. Алматы, Бостандыкский район, улица Хусаинова, д. 225</i>'),

    MessageInput(edit_object_address_input, filter=F.text),

    state=EditObject.edit_address
)

# Окно для редактирования условий и цены объекта
edit_conditions_window = Window(
    Const('<b>Укажите Новые Стоимость и Условия аренды:</b>\n\n'
        '<i>Например: Долгосрочная/среднесрочная аренда. 950 долларов в месяц</i>'),

    MessageInput(edit_object_conditions_input, filter=F.text),

    state=EditObject.edit_conditions
)

# Окно для редактирования описания объекта
edit_description_window = Window(
    Const('<b>Укажите Новое краткое Описание:</b>\n\n'
        '<i>Например: 2 комнаты, 50 ка, свежий ремонт, сантехника новая, стиральная машина, '
        'посудомойка, холодильник, центр города, метро 15 мин дальности, размещение животных не допускается.</i>'),

    MessageInput(edit_object_description_input, filter=F.text),

    state=EditObject.edit_description
)