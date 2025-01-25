from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config

from src.database.models import Base

# создание движка + отключение логов sql
engine = create_async_engine(Config.sqlalchemy_url, echo=False)
async_session = async_sessionmaker(engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)