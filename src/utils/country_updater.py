from pyrogram import Client

from config import Config


# Получаем список всех стран, исходя из названий топиков в чате
async def get_country_list(chat: int | str):
    # Запускаем pyrogram бота
    async with Client(
            name='src/sessions/acc_to_check_topic',
            api_id=Config.api_id,
            api_hash=Config.api_hash
    ) as app:
        # Список для хранения названий стран
        countries = []

        # Получаем все топики форума
        await app.join_chat(chat_id=chat)

        async for topic in app.get_forum_topics(chat_id=chat):
            # Извлекаем название темы
            topic_title = topic.title
            thread_id = topic.id

            # Предполагаем, что название страны выделяется эмодзи (например, флаг)
            # Разделим строку по '|' и берем первую часть
            country_name = topic_title[2:].strip().split('|')
            if len(country_name) < 2:
                continue
            else:
                country_name = country_name[0].strip()

            # Добавляем название страны в список
            countries.append([country_name, thread_id])

        return countries