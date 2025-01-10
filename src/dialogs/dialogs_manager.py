from aiogram_dialog import Dialog

from src.dialogs.windows.create_object import get_country_window, get_type_window, get_address_window, \
    get_conditions_window, get_description_window, get_contacts_window, get_photos_window
from src.dialogs.windows.info import info_window
from src.dialogs.windows.main_menu import main_menu_window
from src.dialogs.windows.objects_manager import objects_manager_window

# Основной диалог у Пользователя
user_dialog = Dialog(
    main_menu_window,

    objects_manager_window,

    info_window
)

# Диалог с созданием нового объекта
create_object_dialog = Dialog(
    get_country_window,
    get_type_window,
    get_address_window,
    get_conditions_window,
    get_description_window,
    get_contacts_window,
    get_photos_window
)