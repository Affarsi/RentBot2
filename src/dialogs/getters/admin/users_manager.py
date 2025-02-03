from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.input import MessageInput

from src.database.requests.user import db_get_user, db_update_user, find_user_by_username
from src.dialogs.dialogs_states import AdminDialog


# Возвращает список всех пользователей для admin scrolling group
async def all_users_getter(dialog_manager: DialogManager, **kwargs):
    all_users_list = await db_get_user()  # Получение списка пользователей из базы данных

    # Преобразование в нужный формат
    formatted_users_list = [
        [f"@{user['username']} [{user['telegram_id']}]", str(user['id'])]
        for user in all_users_list
    ]

    return {'all_users_list': formatted_users_list}


# Сохраняет user_id выбранного Пользователя и открывает новое окно
async def admin_open_user_account(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    # Сохраняем ID выбранного пользователя в dialog_data
    s_user_id = int(item_id)
    dialog_manager.dialog_data['s_user_id'] = s_user_id

    # Следующее окно
    await dialog_manager.switch_to(state=AdminDialog.open_user_account)


# Поиск Пользователя по username
async def search_user_by_username(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    username_for_find = message.text.replace('@', '').strip()
    user_id = await find_user_by_username(username=username_for_find)

    if user_id is None:
        await dialog_manager.event.answer(f'{username_for_find}, не найден!')
    else:
        # Сохраняем ID выбранного пользователя в dialog_data
        s_user_id = user_id
        dialog_manager.dialog_data['s_user_id'] = s_user_id

        # Следующее окно
        await dialog_manager.switch_to(state=AdminDialog.open_user_account)


# Возвращает информацию о выбранном Пользователе
async def user_account_getter(dialog_manager: DialogManager, **kwargs):
    s_user_id = dialog_manager.dialog_data.get('s_user_id') # Получаем s_user_id

    # Получаем все данные о пользователе
    user_data = await db_get_user(user_id=s_user_id)

    return user_data


# Присваивание Пользователю нового статуса
async def new_user_status_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    new_status = message.text.strip() # новый статус
    s_user_id = dialog_manager.dialog_data.get('s_user_id') # user_id

    # Обновляем данные в БД
    await db_update_user(user_id=s_user_id, status=new_status)

    # Переключаем окно
    await dialog_manager.switch_to(state=AdminDialog.open_user_account)


# Присваивание Пользователю нового лимита объектов
async def new_user_obj_limit_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    new_object_limit = message.text.strip()  # новый лимит объектов
    s_user_id = dialog_manager.dialog_data.get('s_user_id')  # user_id

    # Ввел ли Пользователь число?
    try:
        new_object_limit = int(new_object_limit)
    except ValueError:
        await dialog_manager.event.answer('Введите число!')
        return

    # Обновляем данные в БД
    await db_update_user(user_id=s_user_id, object_limit=new_object_limit)

    # Переключаем окно
    await dialog_manager.switch_to(state=AdminDialog.open_user_account)


# Приплюсовывание Пользователю баланса
async def new_user_plus_balance_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    amount = message.text # число, на которое нужно приплюсовать баланс Пользователя
    s_user_id = dialog_manager.dialog_data.get('s_user_id')  # user_id

    # Ввел ли Пользователь число?
    try:
        amount = int(amount)
    except ValueError:
        await dialog_manager.event.answer('Введите число!')
        return

    # Обновляем данные в БД
    await db_update_user(user_id=s_user_id, plus_balance=amount)

    # Переключаем окно
    await dialog_manager.switch_to(state=AdminDialog.open_user_account)
