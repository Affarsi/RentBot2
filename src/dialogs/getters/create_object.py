from random import randrange

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.input import MessageInput

from src.database.requests.country import db_get_country, db_get_country_name_by_id
from src.database.requests.object import db_new_object
from src.dialogs.dialogs_states import CreateObject
from src.utils.media_group_creator import create_media_group


# Очищает информацию, которая собирается при создании объекта
async def clear_dialog_data_create_object(
        callback: CallbackQuery=None,
        widget: Button=None,
        dialog_manager: DialogManager=None
):
    dialog_manager.show_mode = ShowMode.AUTO

    keys_to_remove = [
        'create_object_data_country_id',
        'create_object_data_country_name',
        'create_object_data_type',
        'create_object_data_address',
        'create_object_data_conditions',
        'create_object_data_description',
        'create_object_data_contacts',
        'create_object_data_photos',
        'create_object_data_generate_id'
    ]

    for key in keys_to_remove:
        dialog_manager.dialog_data.pop(key, None)  # Удаляем ключ, если он существует


# Очищает фотографии, полученные при создании объекта
async def clear_photos_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    try:
        dialog_manager.dialog_data.pop('create_object_data_photos')
    except:
        pass


# Возвращает список стран [Название страны, ID страны]
async def country_list_getter(dialog_manager: DialogManager, **kwargs):
    countries = await db_get_country()
    country_list = [[country[1], country[0]] for country in countries]  # Извлекаем ID и название страны
    return {'country_list': country_list}


# Выбор страны и переход к следующему шагу
async def create_object_country_input(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        item_id: str
):
    country_name = await db_get_country_name_by_id(country_id=int(item_id))

    dialog_manager.dialog_data['create_object_data_country_id'] = int(item_id)
    dialog_manager.dialog_data['create_object_data_country_name'] = country_name

    await dialog_manager.switch_to(CreateObject.get_type)
    # await dialog_manager.switch_to(CreateObject.get_photos)


# Выбор типа объекта и переход к следующему шагу
async def create_object_type_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_type = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_type'] = object_type
    await dialog_manager.switch_to(CreateObject.get_address)


# Выбор адреса объекта и переход к следующему шагу
async def create_object_address_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_address = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_address'] = object_address
    await dialog_manager.switch_to(CreateObject.get_conditions)


# Выбор стоимости и условий аренды объекта и переход к следующему шагу
async def create_object_conditions_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_conditions = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_conditions'] = object_conditions
    await dialog_manager.switch_to(CreateObject.get_description)


# Выбор описания объекта и переход к следующему шагу
async def create_object_description_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_description = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_description'] = object_description
    await dialog_manager.switch_to(CreateObject.get_contacts)


# Выбор контактов для связи и переход к следующему шагу
async def create_object_contacts_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_contacts = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_contacts'] = object_contacts
    await dialog_manager.switch_to(CreateObject.get_photos)


# Обработка присланных фотографий от пользователя
async def create_object_photos_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    # Получаем file id фотографии
    file_id = message.photo[-1].file_id

    # Смотрим, были ли ранее отправлены фотографии от Пользователя
    photo_list_dialog_data = dialog_manager.dialog_data.get('create_object_data_photos')

    # Формируем список фотографий
    if not photo_list_dialog_data:
        photo_list_dialog_data = [file_id]
    else:
        photo_list_dialog_data.append(file_id)

    # Утверждаем список фотографий
    dialog_manager.dialog_data['create_object_data_photos'] = photo_list_dialog_data


# Удалить загруженные фотографии
async def dell_photos_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Очищаем фотографии из dialog_data
    try:
        photo_list = dialog_manager.dialog_data.pop('create_object_data_photos')
    except KeyError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return

    # Оповещаем Пользователя
    await dialog_manager.event.answer(f'Количество удаленных фотографий: {len(photo_list)}\n'
                                      f'Теперь вы можете отправить новые фотографии!')


# Выбор фотографий объекта и переход к следующему шагу
async def go_final_result_create_onject(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Получение данных
    try:
        chat_id = dialog_manager.event.message.chat.id
        photo_list = dialog_manager.dialog_data.get('create_object_data_photos')

        if len(photo_list) == 0:
            await dialog_manager.event.answer('У вас нет загруженных фотографий')
            return
    except KeyError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return
    except TypeError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return

    # Формирование ID для объекта
    generate_id = randrange(0, 99999)# формируем id для поста
    dialog_manager.dialog_data['create_object_data_generate_id'] = generate_id

    # Формирование медиа группы
    media_group = await create_media_group(state_data=dialog_manager.dialog_data,
                                           photo_list=photo_list)

    # Отправка медиа группы
    await dialog_manager.event.bot.send_media_group(
        chat_id=chat_id,
        media=media_group
    )
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND # чтобы медиа группа раньше отправилась, чем смс от бота
    await dialog_manager.switch_to(CreateObject.final_result)


# Сохранить и отправить объект на модерацию!
async def submit_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    dialog_manager.show_mode = ShowMode.AUTO

    user_tg_id = dialog_manager.event.from_user.id

    # Сохраняем объект в БД и отправляем его на модерацию
    await db_new_object(object_data=dialog_manager.dialog_data, user_tg_id=user_tg_id)

    # Оповещаем пользователя и закрываем диалог
    await dialog_manager.event.answer('Объект успешно отправлен на модерацию!')
    await clear_dialog_data_create_object(dialog_manager=dialog_manager)
    await dialog_manager.done()

