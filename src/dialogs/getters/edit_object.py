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


# Менеджер edit_object_input
async def edit_object_input(
        message: Message,
        widget: MessageInput or Button,
        dialog_manager: DialogManager,
        field_name: str
):
    # Сохранение измененных данных
    new_value = message.text.strip()
    dialog_manager.dialog_data[f'edit_object_data_{field_name}'] = new_value

    # Получение данных об объекте
    object_id = dialog_manager.dialog_data.get('open_object_id')
    objects_list = await db_get_object(object_id=object_id)
    object_dict_data = objects_list[0]

    # Формирование медиа группы
    media_group = await create_media_group(dict_data=object_dict_data, edit_data=dialog_manager.dialog_data)

    # Отправка медиа группы и диалога с edit_menu
    await dialog_manager.event.bot.send_media_group(
        chat_id=message.chat.id,
        media=media_group
    )
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND  # чтобы медиа группа раньше отправилась, чем смс от бота
    await dialog_manager.switch_to(EditObject.result_and_edit_menu)


# Изменить адрес объекта и перейти к следующему шагу
async def edit_object_address_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(message, widget, dialog_manager, 'address')


# Изменить условия и стоимость объекта и перейти к следующему шагу
async def edit_object_conditions_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(message, widget, dialog_manager, 'conditions')


# Изменить описание объекта и перейти к следующему шагу
async def edit_object_description_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(message, widget, dialog_manager, 'description')


# Сохраняет загруженные пользователям новые фотографии объекта
async def edit_object_photos_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    # Получаем file id фотографии
    file_id = message.photo[-1].file_id

    # Смотрим, были ли ранее отправлены фотографии от Пользователя
    new_photo_list = dialog_manager.dialog_data.get('edit_object_data_photos')

    # Формируем список фотографий
    if not new_photo_list:
        new_photo_list = [file_id]
    else:
        new_photo_list.append(file_id)

    # Утверждаем список фотографий
    dialog_manager.dialog_data['edit_object_data_photos'] = new_photo_list


# Удалить загруженные фотографии
async def dell_photos_edit_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Очищаем фотографии из dialog_data
    try:
        photo_list = dialog_manager.dialog_data.pop('edit_object_data_photos')
    except KeyError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return

    # Оповещаем Пользователя
    await dialog_manager.event.answer(f'Количество удаленных фотографий: {len(photo_list)}\n'
                                      f'Теперь вы можете отправить новые фотографии!')


# Изменить фотографии объекта и перейти к следующему шагу
async def confirm_edit_photo_and_go_to_finaly(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Получение данных
    try:
        photo_list = dialog_manager.dialog_data.get('edit_object_data_photos')
    except KeyError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return

    await edit_object_input(callback.message, widget, dialog_manager, 'photos')