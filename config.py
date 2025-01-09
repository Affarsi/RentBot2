from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str = '7617336613:AAEz95VLn0kAoO7vR_9LQbxz4CXfrIpHKrM'  # test_kwork
    sqlalchemy_url = 'sqlite+aiosqlite:///src/database/db.sqlite3'