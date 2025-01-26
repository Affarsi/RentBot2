from sqlalchemy import select
from src.database.run_db import async_session
from src.database.models import PaymentHistory, User


# Создает новый платеж в базе данных.
async def db_new_payment(
        telegram_id: int,
        order_id: str,
        amount: int
):
    async with async_session() as session:
        # Получение user_id по telegram_id
        user = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = user.scalar()

        new_payment = PaymentHistory(
            user_id=user.id,
            order_id=order_id,
            amount=amount,
        )

        session.add(new_payment)
        await session.commit()


# Обновляет статус платежа в базе данных на success.
async def db_update_payment_success(order_id: str):
    async with async_session() as session:
        payment = await session.execute(
            select(PaymentHistory).where(PaymentHistory.order_id == order_id)
        )
        payment = payment.scalar_one_or_none()

        payment.success = True
        await session.commit()
        return True