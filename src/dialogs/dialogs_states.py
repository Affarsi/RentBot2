from aiogram.fsm.state import State, StatesGroup

class UserPanel(StatesGroup):
    main_menu = State()

    profile = State()
    points_history = State() # история получения баллов

    referrals = State()
    referrals_history = State() # история рефералов

    tasks = State()
    task_info = State() # посмотреть задание

    leaderboard = State()

    info = State()
