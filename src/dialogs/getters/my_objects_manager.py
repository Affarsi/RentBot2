import datetime
from datetime import date
from config import Config

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select

from src.database.requests.object import db_get_object, db_update_object, db_new_object
from src.database.requests.user import db_get_user, db_update_user
from src.dialogs.dialogs_states import CreateObject, UserDialog, EditObject
from src.payments.payment_handler import withdraw_user_balance, InsufficientFundsError
from src.utils.media_group_creator import send_media_group


# Возвращает текст для раздела Информация
async def my_objects_getter(dialog_manager: DialogManager, **kwargs):
    # Инициализируем данные
    telegram_id = dialog_manager.event.from_user.id
    object_list = await db_get_object(telegram_id=telegram_id) # Получение списка объектов из БД
    user_dict = await db_get_user(telegram_id=telegram_id)
    obj_limit = user_dict.get('obj_limit')
    free_objects_count = user_dict.get('free_objects_count')

    # Определяем платное или бесплатное будет создание объекта
    is_admin = False
    if telegram_id in Config.admin_ids:
        # Это Администратор
        is_limit_object_max = False
        is_admin = True
    else:
        # Проверяем, израсходовал ли Пользователь свой лимит объектов?
        is_limit_object_max = True if free_objects_count >= int(obj_limit) else False

    # Сохраняем данные
    dialog_manager.dialog_data['is_limit_object_max'] = is_limit_object_max
    dialog_manager.dialog_data['is_admin'] = is_admin

    # Формируем кнопку
    if is_limit_object_max:
        create_object_btn_text = '➕ Создать объект [100руб. - 365 дней]'
    else:
        create_object_btn_text = '➕ Создать объект [0руб. - Бессрочно]'

    # Если у Пользователя не найдено объектов
    if not object_list:
        return {'not_object': True, 'create_object_btn_text': create_object_btn_text}

    # Формируем список объектов
    my_object_list = []
    for obj in object_list:
        id = obj['id']
        status = obj['status']
        generate_id = obj['generate_id']
        country = obj['country']
        my_object_list.append([f'{status} | ID: {generate_id} | {country}', str(id)])

    return {'not_object': False, 'my_object_list': my_object_list, 'create_object_btn_text': create_object_btn_text}


# Создание объекта. Запуск диалога с созданием объекта
async def start_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Инициализируем данные
    user_dict = await db_get_user(telegram_id=callback.from_user.id)
    user_id = user_dict['id']
    balance = user_dict['balance']
    is_admin = dialog_manager.dialog_data.get('is_admin')
    is_limit_object_max = dialog_manager.dialog_data.get('is_limit_object_max')

    # Проверяем условия и пытаемся списать деньги с баланса Пользователя
    try:
        is_free_create_object = await withdraw_user_balance(
            is_admin=is_admin, is_limit_object_max=is_limit_object_max,
            amount=100, balance=balance, user_id=user_id, callback=callback
        )
    except InsufficientFundsError: return

    # Открытие диалога создания объекта
    await dialog_manager.start(CreateObject.get_country, data={'is_free_create_object': is_free_create_object})


# Вывод информации об объекте Пользователю (send media_group) с меню взаимодействия
async def open_my_object(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    object_id = int(item_id)
    chat_id = dialog_manager.event.message.chat.id

    # Отправка медиа группы
    object_data = await send_media_group(dialog_manager, object_id, chat_id)

    # Сохраняем id открытого объекта
    dialog_manager.dialog_data['open_object_id'] = object_id
    dialog_manager.dialog_data['open_object_data'] = object_data

    # Чтобы медиа группа отправилась раньше чем смс от бота
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    # В зависимости от статуса выводим меню взаимодействия
    if object_data['status'] == '✅':
        await dialog_manager.switch_to(UserDialog.my_open_object_confirmed)
    elif object_data['status'] == '🔄':
        await dialog_manager.switch_to(UserDialog.my_open_object_moderated)
    elif object_data['status'] == '❌':
        await dialog_manager.switch_to(UserDialog.my_open_object_deleted)


# Удалить созданный объект
async def delete_my_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    object_id = dialog_manager.dialog_data.get('open_object_id')
    object_data = dialog_manager.dialog_data.get('open_object_data')

    # Удаление поста с группы
    message_ids = object_data['message_ids']
    message_ids = message_ids.split(', ')
    try:
        await dialog_manager.event.bot.delete_messages(chat_id=Config.chat, message_ids=message_ids)
    except:
        print('Пользователь пытается удалить объект. Скрипт не может найти message_id')

    # Изменяем статус объекта на 'Удалён'
    new_object_data = {'status': '❌', 'delete_reason': 'Удалено инициатором!', 'message_ids': None}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    await dialog_manager.event.answer('Объект успешно удалён!')
    await dialog_manager.back()


# Инверсия переменной is_edit_menu_open
async def invert_edit_menu_open(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    is_edit_menu_open = dialog_manager.dialog_data.get('is_edit_menu_open', False)

    # Инверсируем значение
    dialog_manager.dialog_data['is_edit_menu_open'] = not is_edit_menu_open


# Инверсия переменной is_delete_object_confirm_menu
async def invert_delete_object_confirm_menu(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    is_delete_object_confirm_menu = dialog_manager.dialog_data.get('is_delete_object_confirm_menu', False)

    # Инверсируем значение
    dialog_manager.dialog_data['is_delete_object_confirm_menu'] = not is_delete_object_confirm_menu


# Getter, сообщающий, открыто ли edit_menu/delete_menu или нет
async def object_confirmed_getter(dialog_manager: DialogManager, **kwargs):
    # Инициализация данных
    object_data = dialog_manager.dialog_data.get('open_object_data')
    payment_date = object_data['payment_date']
    is_edit_menu_open = dialog_manager.dialog_data.get('is_edit_menu_open')
    is_delete_object_confirm_menu = dialog_manager.dialog_data.get('is_delete_object_confirm_menu')

    # Вычисляем остаток дней
    if payment_date is None:
        # Бессрочный объект
        days_left = 'Бессрочно'
    else:
        end_date = payment_date + datetime.timedelta(days=365)
        days_left = abs(end_date - payment_date)
        days_left = str(days_left).split(',')[0]

    return {'edit_menu_open': is_edit_menu_open,
            'delete_object_confirm_menu': is_delete_object_confirm_menu,
            'days_left': days_left}


# Вывод данных для открытого удалённого объекта
async def my_object_delete_getter(dialog_manager: DialogManager, **kwargs):
    # Инициализируем данные
    is_limit_object_max = dialog_manager.dialog_data.get('is_limit_object_max')
    is_edit_menu_open = dialog_manager.dialog_data.get('is_edit_menu_open')

    # Определение причины удаления
    delete_reason = dialog_manager.dialog_data.get('open_object_data').get('delete_reason')

    # Формируем кнопку
    if is_limit_object_max:
        edit_object_btn_text = '🔄 Восстановить объект [100руб. - 365 дней]'
        dialog_manager.dialog_data['is_free_edit_object'] = False # Запоминаем, что редактирование платное
    else:
        edit_object_btn_text = '🔄 Восстановить объект [0руб. - Бессрочно]'
        dialog_manager.dialog_data['is_free_edit_object'] = True # Запоминаем, что редактирование бесплатное

    return {'edit_menu_open': is_edit_menu_open, 'delete_reason': delete_reason, 'edit_object_btn_text': edit_object_btn_text}


# Восстановление объекта
async def restore_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Инициализируем данные
    user_dict = await db_get_user(telegram_id=callback.from_user.id)
    user_id = user_dict['id']
    balance = user_dict['balance']
    object_id = dialog_manager.dialog_data.get('open_object_id')
    is_admin = dialog_manager.dialog_data.get('is_admin')
    is_limit_object_max = dialog_manager.dialog_data.get('is_limit_object_max')

    # Проверяем условия и пытаемся списать деньги с баланса Пользователя
    try:
        is_free_edit_object = await withdraw_user_balance(
            is_admin=is_admin, is_limit_object_max=is_limit_object_max,
            amount=100, balance=balance, user_id=user_id, callback=callback
        )
    except InsufficientFundsError: return

    # Восстанавливаем объект и отправляем его снова на модерацию
    payment_date = None if is_free_edit_object else date.today()
    new_object_data = {'status': '🔄', 'payment_date': payment_date, 'delete_reason': None}
    await db_update_object(object_id=object_id, object_data=new_object_data)

    # Возвращаем обратно Пользователя
    await callback.answer('Объект отправлен на модерацию!')
    await dialog_manager.switch_to(state=UserDialog.my_objects_manager)