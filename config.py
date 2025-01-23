from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str = '123'
    sqlalchemy_url: str = 'sqlite+aiosqlite:///src/database/db.sqlite3'
    admin_ids = [123] # IDs список администраторов
    api_id: int = 123
    api_hash: str = '123'
    chat: str or int = "@123" # ID или "@логин чата"

    # Пример ID чата
    # chat: str or int = -109234012098402
    # Пример логин чата
    # chat: str or int = "@klajflksadjflsakdjfklsafd"
