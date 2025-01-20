import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo, Url, Back, ScrollingGroup, Select, Button, Cancel

from src.dialogs.dialogs_states import UserDialog, CreateObject, EditObject, AdminEditObject
from src.dialogs.getters.admin.edit_object import admin_submit_edit_object, \
    admin_edit_object_address_input, admin_edit_object_conditions_input, admin_edit_object_description_input, \
    admin_edit_object_photos_input, dell_photos_admin_edit_object, admin_confirm_edit_photo_and_go_to_finaly
from src.dialogs.getters.edit_object import clear_dialog_data_edit_object

# Итоговый вариант редактирование с admin_edit_menu
admin_result_and_edit_menu_window = Window(
    Const('<b>Выше вы видите отредактированный пост!\n\n</b>'
          'Вы можете отказаться от изменений или отправить его на модерацию'),

    Button(Const('✏️ Меню редактирования'), id='...'),
    Row(
        SwitchTo(Const('Адрес'), id='admin_edit_address', state=AdminEditObject.edit_address),
        SwitchTo(Const('Цена и Условия'), id='admin_edit_conditions', state=AdminEditObject.edit_conditions),
        SwitchTo(Const('Описание'), id='admin_edit_description', state=AdminEditObject.edit_description),
        SwitchTo(Const('Фотографии'), id='admin_edit_photos', state=AdminEditObject.edit_photos),
    ),
    Button(Const('✅ Подтвердить и Изменить/Одобрить'), id='submit_admin_edit_object', on_click=admin_submit_edit_object),
    Cancel(Const('Отменить изменение объекта'), id='stop_admin_edit_object', on_click=clear_dialog_data_edit_object),

    state=AdminEditObject.result_and_edit_menu
)

# Окно для редактирования адреса объекта
admin_edit_address_window = Window(
    Const('<b>Укажите Новый Адрес объекта:</b>\n\n'
          '<i>Например: г. Алматы, Бостандыкский район, улица Хусаинова, д. 225</i>'),

    MessageInput(admin_edit_object_address_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_edit_menu', state=AdminEditObject.result_and_edit_menu),

    state=AdminEditObject.edit_address
)

# Окно для редактирования условий и цены объекта
admin_edit_conditions_window = Window(
    Const('<b>Укажите Новые Стоимость и Условия аренды:</b>\n\n'
        '<i>Например: Долгосрочная/среднесрочная аренда. 950 долларов в месяц</i>'),

    MessageInput(admin_edit_object_conditions_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_edit_menu', state=AdminEditObject.result_and_edit_menu),

    state=AdminEditObject.edit_conditions
)

# Окно для редактирования описания объекта
admin_edit_description_window = Window(
    Const('<b>Укажите Новое краткое Описание:</b>\n\n'
        '<i>Например: 2 комнаты, 50 ка, свежий ремонт, сантехника новая, стиральная машина, '
        'посудомойка, холодильник, центр города, метро 15 мин дальности, размещение животных не допускается.</i>'),

    MessageInput(admin_edit_object_description_input, filter=F.text),

    SwitchTo(Const('Назад'), id='back_to_admin_edit_menu', state=AdminEditObject.result_and_edit_menu),

    state=AdminEditObject.edit_description
)

# Окно для редактирования фотографий объекта
admin_edit_photos_window = Window(
    Const('<b>Отправьте фотографии объекта (от 2 до 8)</b>\n\n'
          'Необходимо сжать и сгруппировать фотографии перед отправкой!\n\n'
          '<b>❗️ Если вы отправили фотографии</b> - то они успешно загружены!\n'
          '<b>❗️ Если вы хотите изменить фотографии</b> - нажмите УДАЛИТЬ ФОТОГРАФИИ и отправьте их снова!\n'
          '<b>❗️ Если вы готовы продолжить</b> - нажмите кнопку ДАЛЕЕ'),

    MessageInput(admin_edit_object_photos_input, filter=F.photo),

    Row(
        Button(Const('🗑 Удалить фотографии'), id='dell_photos_admin_edit_object', on_click=dell_photos_admin_edit_object),
        Button(Const('✅ Далее'), id='go_final_result_admin_edit_object', on_click=admin_confirm_edit_photo_and_go_to_finaly),
    ),
    SwitchTo(Const('Назад'), id='back_to_admin_edit_menu', state=AdminEditObject.result_and_edit_menu),

    state=AdminEditObject.edit_photos
)