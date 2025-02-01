from aiogram.types import CallbackQuery, Message, InlineKeyboardButton

from src.database.requests.user import db_update_user

class InsufficientFundsError(Exception):
    """Исключение, указывающее на недостаток средств."""
    pass

InlineKeyboardButton(text='Связаться', url='https://t.me/VontRianast')

# Пополнить баланс Пользователя
async def deposit_user_balance(
        amount: int,
        callback: CallbackQuery=None,
        message: Message=None,
        user_id: int=None,
        telegram_id: int=None
):
    await db_update_user(user_id=user_id, telegram_id=telegram_id, plus_balance=amount)
    if callback:
        await callback.answer(f'На ваш баланс зачислено: {amount}руб.!')


async def withdraw_user_balance(
        is_admin: bool,
        is_limit_object_max: bool,
        amount: int,
        balance: int,
        user_id: int,
        callback: CallbackQuery
):
    is_free_create_object = False # Создание объекта будет платным
    if not is_admin and is_limit_object_max:
        # Закончился бесплатный лимит
        if balance >= amount:
            # Есть деньги на балансе
            await db_update_user(user_id=user_id, plus_balance=-amount)
            await callback.answer(f'С баланса списано: {amount}руб.!')
        else:
            # Нет денег на балансе
            await callback.answer('На вашем балансе недостаточно средств!')
            raise InsufficientFundsError("На вашем балансе недостаточно средств!")
    else:
        # Есть бесплатный лимит
        is_free_create_object = True # Создание объекта будет бесплатным

    return is_free_create_object
# Списать баланс Пользователя