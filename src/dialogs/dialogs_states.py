from aiogram.fsm.state import State, StatesGroup

class UserDialog(StatesGroup):
    main_menu = State()

    my_objects_manager = State()
    my_open_my_object_confirmed = State()
    my_open_my_object_moderated = State()
    my_open_my_object_deleted = State()

    info = State() # Информационная доска

class AdminDialog(StatesGroup):
    menu = State()

    users_manager = State()
    open_user_account = State()
    change_user_status = State()
    change_user_obj_limit = State()

    all_objects_manager = State()
    all_objects_confirmed = State()
    all_objects_moderated = State()
    all_objects_deleted = State()

class CreateObject(StatesGroup):
    get_country = State()
    get_type = State()
    get_address = State()
    get_conditions = State()
    get_description = State()
    get_contacts = State()
    get_photos = State()
    final_result = State()

class EditObject(StatesGroup):
    result_and_edit_menu = State()
    edit_address = State()
    edit_conditions = State()
    edit_description = State()
    edit_photos = State()
