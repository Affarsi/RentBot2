from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.input import MessageInput

from src.database.requests.object import db_get_object, db_update_object
from src.dialogs.dialogs_states import EditObject, UserDialog
from src.utils.media_group_creator import create_media_group


# Запуск edit_menu_dialog и сохранение open_object_id
async def start_edit_menu_dialog(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    callback_data = callback.data.split('_')[1]

    states = {
        'conditions': EditObject.edit_conditions,
        'description': EditObject.edit_description,
        'contacts': EditObject.edit_contacts,
        'photos': EditObject.edit_photos
    }

    if callback_data in states:
        # Получение данных об объекте
        object_id = dialog_manager.dialog_data.get('open_object_id')
        objects_list = await db_get_object(object_id=object_id)
        object_dict_data = objects_list[0]

        # Начинаем AdminEditObject диалог и передаем start_data
        await dialog_manager.start(state=states[callback_data], data={'open_object_dict_data': object_dict_data,
                                                                      'open_object_id': object_id})


# Очищает информацию, которая собирается при изменении объекта
async def clear_dialog_data_edit_object(
        callback: CallbackQuery=None,
        widget: Button=None,
        dialog_manager: DialogManager=None
):
    dialog_manager.show_mode = ShowMode.AUTO

    keys_to_remove = [
        'open_object_dict_data',
        'edit_object_data_conditions',
        'edit_object_data_description',
        'edit_object_data_contacts',
        'edit_object_data_photos'
    ]

    for key in keys_to_remove:
        dialog_manager.dialog_data.pop(key, None)  # Удаляем ключ, если он существует


# Менеджер edit_object_input
async def edit_object_input(
        widget: MessageInput or Button,
        dialog_manager: DialogManager,
        field_name: str,
        photos: list=None,
        message: Message=None
):
    # Сохранение измененных данных
    if photos is None:
        new_value = message.text.strip()
    else:
        new_value = photos
    dialog_manager.dialog_data[f'edit_object_data_{field_name}'] = new_value

    # Получение данных об объекте
    object_dict_data = dialog_manager.start_data.get('open_object_dict_data')

    # Формирование медиа группы
    media_group = await create_media_group(dict_data=object_dict_data, edit_data=dialog_manager.dialog_data)

    # Отправка медиа группы и диалога с edit_menu
    await dialog_manager.event.bot.send_media_group(
        chat_id=dialog_manager.event.from_user.id,
        media=media_group
    )
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND  # чтобы медиа группа раньше отправилась, чем смс от бота
    await dialog_manager.switch_to(EditObject.result_and_edit_menu)


# Изменить условия и стоимость объекта и перейти к следующему шагу
async def edit_object_conditions_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(widget, dialog_manager, 'conditions', message=message)


# Изменить описание объекта и перейти к следующему шагу
async def edit_object_description_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(widget, dialog_manager, 'description', message=message)


# Изменить контакты объекта и перейти к следующему шагу
async def edit_object_contacts_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    await edit_object_input(widget, dialog_manager, 'contacts', message=message)


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
        if len(photo_list) < 3 or len(photo_list) > 7:
            await dialog_manager.event.answer('Загрузите больше 2ух и не меньше 8 фотографий!')
            return
    except KeyError:
        await dialog_manager.event.answer('У вас нет загруженных фотографий')
        return

    await edit_object_input(widget, dialog_manager, 'photos', photos=photo_list)


# Сохранить и отправить объект на модерацию!
async def submit_edit_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    dialog_manager.show_mode = ShowMode.AUTO

    # Создаем новый словарь
    new_object_data = {'status': '🔄'}
    dialog_data = dialog_manager.dialog_data
    if 'edit_object_data_conditions' in dialog_data:
        new_object_data['conditions'] = dialog_data['edit_object_data_conditions']
    if 'edit_object_data_description' in dialog_data:
        new_object_data['description'] = dialog_data['edit_object_data_description']
    if 'edit_object_data_contacts' in dialog_data:
        new_object_data['contacts'] = dialog_data['edit_object_data_contacts']
    if 'edit_object_data_photos' in dialog_data:
        new_object_data['photos'] = dialog_data['edit_object_data_photos']

    # Сохраняем объект в БД и отправляем его на модерацию
    await db_update_object(object_id=dialog_manager.start_data.get('open_object_id'),
                           object_data=new_object_data)

    # Оповещаем пользователя и закрываем диалог
    await dialog_manager.event.answer('Объект успешно отправлен на модерацию!')
    await clear_dialog_data_edit_object(dialog_manager=dialog_manager)
    await dialog_manager.start(state=UserDialog.my_objects_manager)