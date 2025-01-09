from typing import List
from config import Config
from aiogram.types import Message
from aiogram.filters import BaseFilter

admin_list = Config.admin_ids

class IsAdmin(BaseFilter):
    def __init__(self, user_ids: int | List[int]=admin_list) -> None:
        self.user_ids = user_ids

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.user_ids, int):
            return message.from_user.id == self.user_ids
        return message.from_user.id in self.user_ids