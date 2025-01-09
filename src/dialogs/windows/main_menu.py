from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Start, Group, Row, SwitchTo

from config import Config
from src.dialogs.dialogs_states import UserPanel


# Основное меню Пользователя
main_menu_window = Window(
    Multi(
        Const('<b>👋 Добро пожаловать в Рейтинг Бот!</b>'),
        Const(
            '🏆 Отслеживайте таблицу лидеров\n'
            '💰 Зарабатывайте баллы\n'
            '🎁 Участвуйте в интересных конкурсах'
        ),
        Const('<b>🦸‍♂️Поддержка - @sermseo</b>'),

        sep='\n\n'
    ),

    Group(
        Row(
            SwitchTo(Const('👤 Мой кабинет'), id='profile', state=UserPanel.profile),
            SwitchTo(Const('🤝 Мои рефералы'), id='referrals', state=UserPanel.referrals),
        ),
        SwitchTo(Const('💰 Задания'), id='tasks', state=UserPanel.tasks),
        SwitchTo(Const('🏆 Таблица лидеров'), id='leaderboard', state=UserPanel.leaderboard),
        SwitchTo(Const('📕 Информация (F.A.Q.)'), id='info', state=UserPanel.info),
    ),

    state=UserPanel.main_menu
)