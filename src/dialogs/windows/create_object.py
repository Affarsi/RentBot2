import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Row, Cancel, Select, ScrollingGroup, Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.dialogs_states import CreateObject
from src.dialogs.getters.create_object import (
    stop_create_object, country_list_getter,
    create_object_country_input, create_object_type_input, create_object_address_input, create_object_conditions_input,
    create_object_description_input, create_object_contacts_input, create_object_photos_input,
    dell_photos_create_object, go_final_result_create_onject, submit_create_object
)

# Выбор страны и переход к следующему шагу
get_country_window = Window(
    Const('<b>Выберите страну, в которой будет размещён ваш объект</b>\n\n'
        'Если в списке ниже нет необходимой вам страны - обратитесь к администратору!'),

    Group(
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='s_country_create_object',
                item_id_getter=operator.itemgetter(1),
                items='country_list',
                on_click=create_object_country_input,
            ),
            id='country_list_for_create_object',
            width=2,
            height=7,
        ),
        Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object)
    ),

    getter=country_list_getter,
    state=CreateObject.get_country
)

# Выбор типа объекта и переход к следующему шагу
get_type_window = Window(
    Const('<b>Укажите Тип Объекта:</b>\n\n<i>Например: Квартира 2ух комнатная</i>'),

    MessageInput(create_object_type_input, filter=F.text),

    Back(Const('Назад')),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_type
)

# Выбор адреса объекта и переход к следующему шагу
get_address_window = Window(
    Const('<b>Укажите Адрес объекта:</b>\n\n'
          '<i>Например: г. Алматы, Бостандыкский район, улица Хусаинова, д. 225</i>'),

    MessageInput(create_object_address_input, filter=F.text),

    Back(Const('Назад')),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_address
)

# Выбор стоимости и условий аренды объекта и переход к следующему шагу
get_conditions_window = Window(
    Const('<b>Укажите Стоимость и Условия аренды:</b>\n\n'
        '<i>Например: Долгосрочная/среднесрочная аренда. 950 долларов в месяц</i>'),

    MessageInput(create_object_conditions_input, filter=F.text),

    Back(Const('Назад')),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_conditions
)

# Выбор описания объекта и переход к следующему шагу
get_description_window = Window(
    Const('<b>Укажите краткое Описание:</b>\n\n'
        '<i>Например: 2 комнаты, 50 ка, свежий ремонт, сантехника новая, стиральная машина, '
        'посудомойка, холодильник, центр города, метро 15 мин дальности, размещение животных не допускается.</i>'),

    MessageInput(create_object_description_input, filter=F.text),

    Back(Const('Назад')),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_description
)

# Выбор контактов для связи и переход к следующему шагу
get_contacts_window = Window(
    Const('<b>Укажите контакты для связи:</b>\n\n'
        '<i>Например: Чтобы получить прямой контакт арендодателя пишите @telegra_login</i>'),

    MessageInput(create_object_contacts_input, filter=F.text),

    Back(Const('Назад')),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_contacts
)

# Выбор фотографий объекта и переход к следующему шагу
get_photos_window = Window(
    Const('<b>Отправьте фотографии объекта (от 2 до 8)</b>\n\n'
          'Необходимо сжать и сгруппировать фотографии перед отправкой!\n\n'
          '<b>❗️ Если вы отправили фотографии</b> - то они успешно загружены!\n'
          '<b>❗️ Если вы хотите изменить фотографии</b> - нажмите УДАЛИТЬ ФОТОГРАФИИ и отправьте их снова!\n'
          '<b>❗️ Если вы готовы продолжить</b> - нажмите кнопку ДАЛЕЕ'),

    MessageInput(create_object_photos_input, filter=F.photo),

    Row(
        Button(Const('🗑 Удалить фотографии'), id='dell_photos_create_object', on_click=dell_photos_create_object),
        Button(Const('✅ Далее'), id='go_final_result_create_object', on_click=go_final_result_create_onject),
    ),
    Back(Const('Назад'), on_click=stop_create_object),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.get_photos
)

# Финальный осмотр созданного объекта и переход к следующему шагу
final_result_window = Window(
    Const('<b>Выше вы видите пост, который будет отправлен на модерацию.\n</b>'
          '<b>Вы сможете отслеживать его статус в разделе "Мои объекты"\n\n</b>'
          '<b>Выберите действие:</b>'),

    Button(Const('✅ Отправить на модерацию'), id='submit_create_object', on_click=submit_create_object),
    Cancel(Const('Прекратить создание объекта'), id='stop_create_object', on_click=stop_create_object),

    state=CreateObject.final_result
)
