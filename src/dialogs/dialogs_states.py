from aiogram.fsm.state import State, StatesGroup

class UserDialog(StatesGroup):
    main_menu = State()

    objects_manager = State()
    open_my_object_confirmed = State()
    open_my_object_moderated = State()
    open_my_object_deleted = State()

    info = State() # Информационная доска

class AdminDialog(StatesGroup):
    menu = State()

    users_manager = State()

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
