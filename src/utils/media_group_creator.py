from typing import List

from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager

from config import Config
from src.database.requests.object import db_get_object


# Формирование описание из информации объекта
async def create_description_for_obj(
        dict_data: dict=None,
        state_data: dict=None,
        edit_data: dict=None
):
    # Возвращает значение с приоритетом edit_data, затем state_data, затем dict_data.
    def get_priority_value(key, default_value):
        edit_key = f'edit_object_data_{key}'
        state_key = f'create_object_state_data_{key}'

        if edit_data and edit_key in edit_data:
            return edit_data[edit_key]
        if state_data and state_key in state_data:
            return state_data[state_key]
        return default_value

    # Убедитесь, что dict_data не None, если да - используйте пустой словарь
    dict_data = dict_data or {}

    # Получение данных объекта
    obj_type = get_priority_value('type', dict_data.get('obj_type'))
    country = get_priority_value('country_name', dict_data.get('country'))
    address = get_priority_value('address', dict_data.get('address'))
    conditions = get_priority_value('conditions', dict_data.get('conditions'))
    description = get_priority_value('description', dict_data.get('description'))
    contacts = get_priority_value('contacts', dict_data.get('contacts'))
    generate_id = get_priority_value('generate_id', dict_data.get('generate_id'))

    # Формирование текста
    caption = (f"<b>🏢 {obj_type} (ID{generate_id})</b>\n"
               f"<b>📍 Местоположение:</b>\n"
               f"{country}, {address}\n"
               f"💸<b> Цена и условия:</b>\n"
               f"{conditions}\n"
               f"<b>🛋 Описание:</b>\n"
               f"{description}\n\n"
               f"<b>☎️ Контакты:</b>\n"
               f"{contacts}")

    return caption


# Формирование медиа группы с информацией об объекте
async def create_media_group(
        dict_data: dict = None,
        state_data: dict = None,
        photo_list: List[str] = None,
        edit_data: dict = None
):
    # Формирование описания
    caption = await create_description_for_obj(dict_data, state_data, edit_data)

    # Формирование медиа группы
    media_group = MediaGroupBuilder(caption=caption)

    # Работа с фотографиями
    if photo_list is None:
        if edit_data is None or 'edit_object_data_photos' not in edit_data:
            photo_list = dict_data['photos']
            photo_list = photo_list.split(', ')
        else:
            photo_list = edit_data['edit_object_data_photos']

    # Сохраняем фотографии в медиа группе
    for photo in photo_list:
        media_group.add_photo(media=photo)

    # Собираем и выводим медиа группу
    media_group = media_group.build()
    return media_group


# Отправка медиа группы
async def send_media_group(
        dialog_manager: DialogManager,
        object_id: int,
        chat_id: int | str,
        send_to_chat: bool=False
) -> dict:
    # Сбор данных
    object_data = await db_get_object(object_id=object_id)
    object_data = object_data[0]

    # Получение message_thread_id
    if send_to_chat:
        message_thread_id = object_data.get('country_thread_id')
    else:
        message_thread_id = None

    # Создание media_group
    media_group = await create_media_group(dict_data=object_data)

    # Отправка media_group
    result = await dialog_manager.event.bot.send_media_group(
        chat_id=chat_id,
        message_thread_id=message_thread_id,
        media=media_group,
    )

    if send_to_chat:
        # Удаляем предыдущие посты!
        old_message_ids = object_data.get('message_ids')
        if old_message_ids:
            try:    # удаляем медиа группу старых сообщений
                await dialog_manager.event.bot.delete_messages(Config.chat, old_message_ids)
            except:
                try:    # если там только одно сообщение - удаляем одно сообщение
                    await dialog_manager.event.bot.delete_message(Config.chat, old_message_ids)
                except:    # если произошла какая-та ошибка
                    print('Не смог удалить старые сообщения, когда админ одобрял или изменял объект')

        # Сохраняем message_ids
        message_ids = []
        for msg in result:
            message_ids.append(str(msg.message_id))
        message_ids_str = ', '.join(message_ids)
        object_data['message_ids'] = message_ids_str

    return object_data