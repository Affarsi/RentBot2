from aiogram_dialog import Dialog

from src.dialogs.windows.admin.all_objects_manager import all_objects_manager_window, all_objects_confirmed_window, \
    all_objects_moderated_window, all_objects_deleted_window, admin_open_object_deleted_window, \
    admin_open_object_confirmed_window, admin_open_object_moderated_window, \
    object_reject_reason_window, object_delete_reason_window
from src.dialogs.windows.admin.edit_object import admin_result_and_edit_menu_window, admin_edit_address_window, \
    admin_edit_conditions_window, admin_edit_description_window, admin_edit_photos_window
from src.dialogs.windows.admin.main_menu import admin_menu_window, update_info_window
from src.dialogs.windows.admin.users_manager import users_manager_window, open_user_account_window, \
    change_user_status_window, change_user_obj_limit_window
from src.dialogs.windows.create_object import get_country_window, get_type_window, get_address_window, \
    get_conditions_window, get_description_window, get_contacts_window, get_photos_window, final_result_window
from src.dialogs.windows.edit_object import edit_conditions_window, edit_description_window, \
    result_and_edit_menu_window, edit_photos_window, edit_contacts_window
from src.dialogs.windows.main_menu import main_menu_window, info_window
from src.dialogs.windows.my_objects_manager import my_objects_manager_window, my_object_confirmed_window, \
    my_object_moderated_window, my_object_deleted_window

# Основной диалог у Пользователя
user_dialog = Dialog(
    main_menu_window,

    my_objects_manager_window,
    my_object_confirmed_window,
    my_object_moderated_window,
    my_object_deleted_window,

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
    get_photos_window,
    final_result_window
)

# Диалог редактирования существующего объекта
edit_object_dialog = Dialog(
    result_and_edit_menu_window,
    edit_conditions_window,
    edit_description_window,
    edit_contacts_window,
    edit_photos_window
)

# Основной диалог у Администратора
admin_dialog = Dialog(
    admin_menu_window,

    users_manager_window,
    open_user_account_window,
    change_user_status_window,
    change_user_obj_limit_window,

    all_objects_manager_window,
    all_objects_confirmed_window,
    all_objects_moderated_window,
    all_objects_deleted_window,
    admin_open_object_confirmed_window,
    admin_open_object_moderated_window,
    admin_open_object_deleted_window,
    object_reject_reason_window,
    object_delete_reason_window,

    update_info_window
)

# Диалог редактирования существующего объекта для Администратора
admin_edit_object_dialog = Dialog(
    admin_result_and_edit_menu_window,
    admin_edit_conditions_window,
    admin_edit_description_window,
    admin_edit_contacts_window,
    admin_edit_photos_window
)