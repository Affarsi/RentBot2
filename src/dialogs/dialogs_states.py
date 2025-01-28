from aiogram.fsm.state import State, StatesGroup

# Основные состояния Пользователя
class UserDialog(StatesGroup):
    main_menu = State()

    my_objects_manager = State()
    my_open_object_confirmed = State()
    my_open_object_moderated = State()
    my_open_object_deleted = State()

    info = State() # Информационная доска

# Отдельные состояния для создания объекта
class CreateObject(StatesGroup):
    get_country = State()
    get_type = State()
    get_address = State()
    get_conditions = State()
    get_description = State()
    get_contacts = State()
    get_photos = State()
    final_result = State()

# Отдельные состояния для изменения объекта
class EditObject(StatesGroup):
    result_and_edit_menu = State()
    edit_conditions = State()
    edit_description = State()
    edit_contacts = State()
    edit_photos = State()

# Основной диалог для Администратора
class AdminDialog(StatesGroup):
    menu = State()

    users_manager = State()
    open_user_account = State()
    change_user_status = State()
    change_user_obj_limit = State()
    change_user_balance = State()

    all_objects_manager = State()
    all_objects_confirmed = State()
    all_objects_moderated = State()
    all_objects_deleted = State()
    admin_open_object_confirmed = State()
    admin_open_object_moderated = State()
    admin_open_object_deleted = State()
    enter_object_reject_reason = State()
    enter_object_delete_reason = State()

    update_info = State()

# Отдельные состояния для изменения объекта для Администратора
class AdminEditObject(StatesGroup):
    result_and_edit_menu = State()
    edit_conditions = State()
    edit_description = State()
    edit_contacts = State()
    edit_photos = State()

# Пополнение баланса
class Payment(StatesGroup):
    main = State()
    waiting_payment = State()