import asyncio
from random import randrange

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message, ReactionType, ReactionTypeEmoji
from aiogram_dialog.widgets.input import MessageInput, TextInput

from src.database.requests.country import db_get_country, db_get_country_name_by_id
from src.database.requests.object import db_new_object, db_get_object
from src.dialogs.dialogs_states import CreateObject, EditObject
from src.utils.media_group_creator import create_media_group


# Изменить адрес объекта и перейти к следующему шагу
async def edit_object_address_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    # Сохраняем измененные данные
    new_address = message.text.strip()
    dialog_manager.dialog_data['edit_object_data_address'] = new_address

    # Получение данных об объекта
    object_id = dialog_manager.dialog_data.get('open_object_id')
    objects_list = await db_get_object(object_id=object_id)
    object_dict_data = objects_list[0]

    # Формирование медиа группы
    media_group = await create_media_group(dict_data=object_dict_data, edit_data=dialog_manager.dialog_data)

    # Отправка медиа группы и диалога с edit_menu
    await dialog_manager.event.bot.send_media_group(
        chat_id=dialog_manager.event.chat.id,
        media=media_group
    )
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND # чтобы медиа группа раньше отправилась, чем смс от бота
    await dialog_manager.switch_to(EditObject.result_and_edit_menu)


# Изменить условия и стоимость объекта и перейти к следующему шагу
async def edit_object_conditions_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_description = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_description'] = object_description
    await dialog_manager.switch_to(CreateObject.get_contacts)


# Изменить описание объекта и перейти к следующему шагу
async def edit_object_description_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    object_description = message.html_text.strip()
    dialog_manager.dialog_data['create_object_data_description'] = object_description
    await dialog_manager.switch_to(CreateObject.get_contacts)