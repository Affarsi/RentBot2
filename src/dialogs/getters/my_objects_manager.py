import datetime
from datetime import date
from config import Config

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select

from src.database.requests.object import db_get_object, db_update_object
from src.database.requests.user import db_get_user, db_update_user
from src.dialogs.dialogs_states import CreateObject, UserDialog
from src.utils.media_group_creator import send_media_group


# Возвращает текст для раздела Информация
async def my_objects_getter(dialog_manager: DialogManager, **kwargs):
    # Инициализируем данные
    telegram_id = dialog_manager.event.from_user.id
    object_list = await db_get_object(telegram_id=telegram_id) # Получение списка объектов из БД
    user_dict = await db_get_user(telegram_id=telegram_id)
    obj_limit = user_dict.get('obj_limit')

    # Если у Пользователя не найдено объектов
    if not object_list:
        return {'my_object_list': [['У вас нет объектов', 1]]}

    # Формируем список объектов
    my_object_list = []
    for obj in object_list:
        id = obj['id']
        status = obj['status']
        generate_id = obj['generate_id']
        country = obj['country']
        my_object_list.append([f'{status} | ID: {generate_id} | {country}', str(id)])

    # Проверка на Администратора
    if telegram_id in Config.admin_ids:
        is_limit_object_max = False
    else:
        # Проверяем, израсходовал ли Пользователь свой лимит объектов?
        is_limit_object_max = True if len(my_object_list) >= int(obj_limit) else False

    return {'my_object_list': my_object_list, 'is_limit_object_max': is_limit_object_max}


# Запускает диалог с созданием объекта
async def start_create_object(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    # Инициализируем данные
    telegram_id = callback.from_user.id
    user_dict = await db_get_user(telegram_id=callback.from_user.id)
    user_id = user_dict['id']
    obj_max = int(user_dict['obj_limit'])
    obj_len = user_dict['obj_list_len']
    balance = user_dict['balance']

    is_free_create_object = False # Создание объекта будет платным
    is_admin = False # Пользователь не Администратор

    # Проверка на Администратора
    if telegram_id in Config.admin_ids:
        is_admin = True
        is_free_create_object = True

    # Проверка условий
    if not is_admin and obj_len >= obj_max:
        # Закончился бесплатный лимит
        if balance >= 100:
            # Есть деньги на балансе
            await db_update_user(user_id=user_id, plus_balance=-100) # Списываем 100 рублей с баланса
            await callback.answer('С баланса списано: 100руб.!')
        else:
            # Нет денег на балансе
            await callback.answer('На вашем балансе недостаточно средств!')
            return
    else:
        # Есть бесплатный лимит
        is_free_create_object = True # Создание объекта будет бесплатным

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
    else:
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
    create_date = object_data['create_date']
    is_edit_menu_open = dialog_manager.dialog_data.get('is_edit_menu_open')
    is_delete_object_confirm_menu = dialog_manager.dialog_data.get('is_delete_object_confirm_menu')

    # Вычисляем остаток дней
    if create_date is None:
        # Бессрочный объект
        days_left = 'Бессрочно'
    else:
        end_date = create_date + datetime.timedelta(days=365)
        days_left = abs(end_date - create_date)
        days_left = str(days_left).split(',')[0]

    return {'edit_menu_open': is_edit_menu_open,
            'delete_object_confirm_menu': is_delete_object_confirm_menu,
            'days_left': days_left}


# Получить причину удаления объекта
async def my_object_delete_reason_getter(dialog_manager: DialogManager, **kwargs):
    delete_reason = dialog_manager.dialog_data.get('open_object_data').get('delete_reason')
    return {'delete_reason': delete_reason}