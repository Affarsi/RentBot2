import hashlib
import requests


url = "https://securepay.tinkoff.ru/v2/CheckOrder"

terminal_key = "1737740259529DEMO"
secret_key = "Qu9g^zQS&TRtnyCp"
order_id = '123451-n67890'

values = {
    # 'Amount':
    # 'Description':
    'OrderId': order_id,
    'Password': secret_key,
    'TerminalKey': terminal_key
}

concatenated_values = ''.join([values[key] for key in (values.keys())])
hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
token = hash_object.hexdigest()
response = requests.post(url, json={'TerminalKey': terminal_key, 'OrderId': order_id, 'Token': token})

if response.status_code == requests.codes.ok:
    response_data = response.json()
    print(response_data)