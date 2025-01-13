import random
from typing import List

from aiogram.utils.media_group import MediaGroupBuilder


# Формирование описание из информации объекта
async def create_description_for_obj(
        dict_data: dict=None,
        state_data: dict=None,
        edit_data: dict=None
):
    # Возвращает значение с приоритетом edit_data, затем state_data, затем dict_data.
    def get_priority_value(key, default_value):
        edit_key = f'edit_object_data_{key}'
        state_key = f'state_object_data_{key}'

        if edit_data and edit_key in edit_data:
            return edit_data[edit_key]
        if state_data and state_key in state_data:
            return state_data[state_key]
        return default_value

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


# Формирование медиа группы c информацией об объекте
async def create_media_group(
        dict_data: dict=None,
        state_data: dict=None,
        photo_list: List[str]=None,
        edit_data: dict=None
):
    # Формирование описания
    caption = await create_description_for_obj(dict_data, state_data, edit_data)

    # Формирование медиа группы
    media_group = MediaGroupBuilder(caption=caption)

    # Работа с фотографиями
    if photo_list is None:
        photo_list = dict_data['photos']
        photo_list = photo_list.split(', ')

    for photo in photo_list:
        media_group.add_photo(media=photo)

    media_group = media_group.build()
    return media_group