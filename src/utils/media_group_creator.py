import random
from typing import List

from aiogram.utils.media_group import MediaGroupBuilder


# Формирование описание из информации объекта
async def create_description_for_obj(dict_data: dict=None, state_data: dict=None):
    # Получение данных объекта
    ojb_type = state_data['obj_type'] if state_data else dict_data['obj_type']
    country = state_data['country'] if state_data else dict_data['country']
    address = state_data['address'] if state_data else dict_data['address']
    conditions = state_data['conditions'] if state_data else dict_data['conditions']
    description = state_data['description'] if state_data else dict_data['description']
    contacts = state_data['contacts'] if state_data else dict_data['contacts']
    generate_id = state_data['contacts'] if state_data else dict_data['contacts']

    # Формирование текста
    caption = (f"<b>🏢 {ojb_type} (ID{generate_id})</b>\n"
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
async def create_media_group(dict_data: dict=None, state_data: dict=None, photo_list: List[str]=None):
    # Формирование описания
    caption = await create_description_for_obj(dict_data, state_data)

    # Формирование медиа группы
    media_group = MediaGroupBuilder(caption=caption)

    for photo in photo_list:
        media_group.add_photo(media=photo)

    media_group = media_group.build()

    return media_group