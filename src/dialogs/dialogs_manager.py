from aiogram_dialog import Dialog

from src.dialogs.windows.main_menu import main_menu_window
from src.dialogs.windows.profile import profile_window

user_panel_dialog = Dialog(
    main_menu_window,

    profile_window,

    # referrals_window,
    # # referrals_history_window,
    #
    # tasks_window,
    # # task_info_window,
    #
    # leaderboard_window,
    #
    # info_window
)