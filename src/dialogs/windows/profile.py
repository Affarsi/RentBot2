from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Start, Group, Row, Back, SwitchTo

from config import Config
from src.dialogs.dialogs_states import UserPanel
from src.dialogs.getters.profile import profile_info


# Информация о профиле
profile_window = Window(
    StaticMedia(path='user_rank_image.jpg'),

    Multi(
        Const('➖➖➖➖➖➖➖➖➖➖➖➖➖'),
        Format('👤 Логин: <code>{user_username}</code>'),
        Format('🕜 Регистрация: <code>{user_invite_date}</code>'),
        Const('➖➖➖➖➖➖➖➖➖➖➖➖➖'),
        Format('💰 Баллы (EXP): <code>{user_points}</code>'),
        Format('🤝 Количество рефералов: <code>{user_referrals}</code>'),
        Const('➖➖➖➖➖➖➖➖➖➖➖➖➖'),
    ),

    Group(
        Back(Const('🔙 Назад'), id='back')
    ),

    getter=profile_info,
    state=UserPanel.profile
)