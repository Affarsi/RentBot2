from dataclasses import dataclass

@dataclass
class Config:
    # Основные настройки
    admin_ids = [6094120092] # IDs список администраторов
    chat: str or int = "@sdafsfdasdfasdfasfd" # -109234012098402 или "@klajflksadjflsakdjfklsafd"
    price_amount = 100 # Цена на создание/продление/восстановление объекта в рублях

    # Технические настройки
    bot_token: str = '7617336613:AAEz95VLn0kAoO7vR_9LQbxz4CXfrIpHKrM'  # test_kwork
    sqlalchemy_url: str = 'sqlite+aiosqlite:///src/database/db.sqlite3'
    api_id: int = 23988290 # МОИ
    api_hash: str = '62b3cc11b049d4e2f5d4a1de5636df06' # МОИ