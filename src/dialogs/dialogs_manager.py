from aiogram_dialog import Dialog

from src.dialogs.windows.info import info_window
from src.dialogs.windows.main_menu import main_menu_window
from src.dialogs.windows.objects_manager import objects_manager_window

user_dialog = Dialog(
    main_menu_window,

    objects_manager_window,

    info_window
)