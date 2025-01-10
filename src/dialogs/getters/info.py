from src.database.requests.settings import db_get_info


# Возвращает текст для раздела Информация
async def info_getter(**kwargs):
    res = {'info': await db_get_info()}
    return res