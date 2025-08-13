from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str = ''  # test_kwork
    sqlalchemy_url: str = 'sqlite+aiosqlite:///src/database/db.sqlite3'
    admin_ids = [902966420, 6094120092] # IDs список администраторов
    api_id: int = 23988290 # МОИ
    api_hash: str = '62b3cc11b049d4e2f5d4a1de5636df06' # МОИ
    chat: str or int = "@sdafsfdasdfasdfasfd" # ID или "@логин чата"

    # Пример ID чата
    # chat: str or int = "@klajflksadjflsakdjfklsafd"

    # Пример логин чата
    # chat: str or int = -109234012098402
