import hashlib
from typing import Optional, Union

import requests
import json

from collections import OrderedDict

TINKOFF_TERMINAL_KEY = "1737740259556"
TINKOFF_TERMINAL_PASSWORD = "LbyrxXU56!FTAq&h"
TINKOFF_INIT_URL = "https://securepay.tinkoff.ru/v2/Init"
TINKOFF_CHECK_ORDER_URL = "https://securepay.tinkoff.ru/v2/CheckOrder"


# Формирование платежа
async def create_payment_link(
        amount: int,
        order_id: str
) -> Union[str, bool]:
    data = OrderedDict({
        'Amount': int(amount * 100),  # Копейки!
        'Description': 'Пополнение баланса Telegram Бота',
        'OrderId': order_id,
        'Password': TINKOFF_TERMINAL_PASSWORD,
        'TerminalKey': TINKOFF_TERMINAL_KEY
    })

    try:
        values = list(data.values())
        concatenated_string = "".join(map(str, values))  # Важно преобразовать в строки
        hashed_string = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()

        data["Token"] = hashed_string
        del data["Password"]  # Удаляем пароль после хеширования

        data = json.dumps(data, ensure_ascii=False)

        response = requests.post(
            TINKOFF_INIT_URL,
            headers={'Content-Type': 'application/json'},
            data=data,
        )
        response.raise_for_status()

        output_array = response.json()
        if output_array.get("Success") is True and "PaymentURL" in output_array:
            return output_array["PaymentURL"]
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса при создании платежа: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON при создании платежа: {e}")
        return False


# Проверка платежа
async def check_payment(order_id: str) -> Union[dict, bool]:
    values = {
        'OrderId': order_id,
        'Password': TINKOFF_TERMINAL_PASSWORD,
        'TerminalKey': TINKOFF_TERMINAL_KEY
    }

    concatenated_values = ''.join([str(values[key]) for key in values.keys()]) #Важно преобразовать в строку
    hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
    token = hash_object.hexdigest()

    try:
        response = requests.post(TINKOFF_CHECK_ORDER_URL, json={'TerminalKey': TINKOFF_TERMINAL_KEY, 'OrderId': order_id, 'Token': token})
        response.raise_for_status() # Поднимает исключение для ошибок кода ответа
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса при проверки платежа: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON при проверки платежа: {e}")
        return False