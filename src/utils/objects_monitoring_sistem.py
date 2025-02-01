from datetime import datetime, date, timedelta

from aiogram import Bot

from src.database.requests.object import db_get_object, db_update_object
from src.database.requests.user import db_get_user, db_update_user
from src.payments.payment_handler import withdraw_user_balance


# Анализирует даты платежей и группирует объекты по статусу срока действия
async def payment_date_analysis(all_objects_list: list):
    today = datetime.today().date()
    results = {
        "warning_14_days": [],
        "warning_7_days": [],
        "warning_1_day": [],
        "expired_objects": []
    }

    for obj in all_objects_list:
        if obj.get('status') != '✅':
            continue

        payment_date = obj.get("payment_date")
        if not isinstance(payment_date, date):
            continue  # Пропускаем объекты с некорректной датой

        print(f"payment_date -- {payment_date}")
        expiration_date = payment_date + timedelta(days=365)  # Вычисляем дату окончания действия
        print(f"expiration_date -- {expiration_date}")
        days_left = (expiration_date - today).days
        print(f"days_left -- {days_left}")

        if days_left == 14:
            results["warning_14_days"].append({
                "owner_telegram_id": obj["owner_telegram_id"],
                "generate_id": obj["generate_id"],
                "object_id": obj['id']
            })
        elif days_left == 7:
            results["warning_7_days"].append({
                "owner_telegram_id": obj["owner_telegram_id"],
                "generate_id": obj["generate_id"],
                "object_id": obj['id']
            })
        elif days_left == 1:
            results["warning_1_day"].append({
                "owner_telegram_id": obj["owner_telegram_id"],
                "generate_id": obj["generate_id"],
                "object_id": obj['id']
            })
        elif days_left <= 0:
            results["expired_objects"].append({
                "owner_telegram_id": obj["owner_telegram_id"],
                "generate_id": obj["generate_id"],
                "object_id": obj['id']
            })

    return results


# Отправляет уведомление пользователю
async def send_notification(bot: Bot, user_id: int, generate_id: str, message: str):
    try:
        await bot.send_message(user_id, message)
        print('Отправил сообщение')
    except Exception as e:
        print(f"Ошибка при отправке уведомления пользователю {user_id}: {e}")


# Мониторинг объектов и уведомления пользователей о статусе подписки
async def objects_monitoring(bot: Bot):
    all_objects_list = await db_get_object()
    warning_objects_dict = await payment_date_analysis(all_objects_list)
    print(warning_objects_dict)

    # Реагируем на объекты с оканчивающимся сроком
    for obj_list, days in zip(
            [
                warning_objects_dict["warning_1_day"],
                warning_objects_dict["warning_7_days"],
                warning_objects_dict["warning_14_days"],
            ],
            ["1", "7", "14"],
    ):
        for obj in obj_list:
            user_id = obj["owner_telegram_id"]
            generate_id = obj["generate_id"]
            await send_notification(
                bot,
                user_id,
                generate_id,
                f'⚠️ <b>Объект: ID{generate_id}</b>\n'
                f'Срок действия вашего объекта истекает через <code>{days}дн.</code>!\n'
                f'Вкл. автопродление, чтобы он не удалился'
            )

    # Реагируем на объекты с истекшим сроком
    for obj in warning_objects_dict["expired_objects"]:
        user_id = obj["owner_telegram_id"]
        generate_id = obj["generate_id"]
        object_id = obj['object_id']
        user_dict = await db_get_user(telegram_id=user_id)
        balance = user_dict.get('balance')
        amount = 100
        recurring_payments = user_dict.get('recurring_payments')

        # включено ли автопродление?
        if recurring_payments:
            # пытаемся списать деньги
            if balance >= amount:
                # Есть деньги на балансе
                await db_update_user(telegram_id=user_id, plus_balance=-amount)

                # Обновляем дату платежа
                await db_update_object(object_id, object_data={'payment_date': date.today()})

                # Оповещаем пользователя
                await bot.send_message(user_id, f'✅ <b>Объект: ID{generate_id}</b>\n'
                                                f'Был успешно продлен!\n'
                                                f'С вашего баланса списано <code>100руб.</code>!')

                continue
        # не получилось

        # изменяем информацию об объекте в БД
        await db_update_object(object_id, object_data={"status": "❌", "delete_reason": "Истек срок размещения!"})

        # уведомление пользователю
        await send_notification(
            bot,
            user_id,
            generate_id,
            f'❌ <b>Объект: ID{generate_id}</b>\n'
            f'Срок действия вашего объекта истек!\n'
            f'Вы можете восстановить его в любое время в разделе <code>"Мои объекты"</code>'
        )