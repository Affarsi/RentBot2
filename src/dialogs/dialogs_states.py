from aiogram.fsm.state import State, StatesGroup

class UserDialog(StatesGroup):
    main_menu = State()

    objects_manager = State()

    info = State() # Информационная доска

class CreateObject(StatesGroup):
    get_country = State()
    get_type = State()
    get_address = State()
    get_conditions = State()
    get_description = State()
    get_contacts = State()
    get_photos = State()
    final_result = State()
