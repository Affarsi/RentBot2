import operator

from aiogram_dialog import Window

from aiogram_dialog.widgets.kbd import Group, Cancel, Select, ScrollingGroup, Button, Counter
from aiogram_dialog.widgets.text import Const, Format
from nextcord.ext.commands import CommandOnCooldown

from src.dialogs.dialogs_states import UpgradeTariff
from src.dialogs.getters.create_object import clear_dialog_data_create_object, create_object_country_input

# Основное меню для улучшения тарифов
upgrade_tariff_main_window = Window(
    Const(
      '🔑 <b>Статус «Владелец» - для всех пользователей!</b> Если вы являетесь владельцем недвижимости, то для вас '
      'первая публикация будет <b>совершенно бесплатной</b>! Успейте поделиться информацией о вашем объекте.\n\n'
      '💡 <b>Статус «Агент» - для владельцев нескольких объектов:</b>\n'
      'Если у вас в распоряжении несколько объектов, мы предлагаем гибкую линейку тарифов, которая подойдёт именно вам:\n'
      '<b>500 руб.</b> – повысить лимит на <b>5 объектов </b>(по 100 руб. за объект)\n'
      '<b>900 руб. </b>– повысить лимит на <b>10 объектов</b> (по 90 руб. за объект)\n'
      '<b>1200 руб.</b> – повысить лимит на <b>15 объектов</b> (по 80 руб. за объект)\n\n'
      'Сумма вносится <b>единоразово</b>, и вы сможете публиковать ваши объекты в течение <b>одного года</b> с момента '
      'пополнения. Обратите внимание: остаток на балансе аннулируется по истечении срока.\n\n'
      '🔄 Опубликованные объекты не удаляются, но вы можете удалить их в любое время через личный кабинет, если это необходимо.'
    ),

    Button(Const('✨ 500 руб. - 5 объектов на 1 год'), id='123', on_click=...),
    Button(Const('✨ 900 руб. - 10 объектов на 1 год'), id='123', on_click=...),
    Button(Const('✨ 1200 руб. - 15 объектов на 1 год'), id='123', on_click=...),
    Counter(id='counter'),
    Button(Const('Выбрать количество самостоятельно'), id='123', on_click=...),
    Cancel(Const('Назад'), id='start_main_menu_dialog'),

    state=UpgradeTariff.main
)