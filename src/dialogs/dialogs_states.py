from aiogram.fsm.state import State, StatesGroup

class User(StatesGroup):
    main_menu = State()

    objects_manager = State()

    info = State() # Информационная доска