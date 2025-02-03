import requests
import json
import hashlib
from collections import OrderedDict

TINKOFF_TERMINAL_KEY = "1737740259529DEMO" # Замените на свой ключ
TINKOFF_TERMINAL_PASSWORD = "Qu9g^zQS&TRtnyCp" # Замените на свой пароль
TINKOFF_INIT_URL = "https://securepay.tinkoff.ru/v2/Init" # Или другой URL, если нужно


def tinkoff_get_link(amount, chat_id, order_number):

    data = OrderedDict({ # OrderedDict для сохранения порядка ключей
        "Amount": int(amount * 100),
        "Description": 'Пополнение баланса бота "Мониторинг сайта"',
        "OrderId": f"{chat_id}-n{order_number}",
        "Password": TINKOFF_TERMINAL_PASSWORD,
        "TerminalKey": TINKOFF_TERMINAL_KEY
    })
    values = list(data.values())
    concatenated_string = "".join(map(str, values))
    hashed_string = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()

    data["Token"] = hashed_string
    del data["Password"]
    data = json.dumps(data, ensure_ascii=False)
    print(data)

    try:
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
            print("Ошибка от Тинькофф:", output_array) # Вывод ошибки для отладки
            return False

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return False

    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return False



# Пример использования
amount = 100
chat_id = 111111
order_number = 11111

payment_url = tinkoff_get_link(amount, chat_id, order_number)

if payment_url:
    print(f"Ссылка на оплату: {payment_url}")
else:
    print("Не удалось получить ссылку на оплату")