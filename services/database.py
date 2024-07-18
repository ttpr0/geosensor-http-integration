from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import config
from models import META_DATA

ENGINE = None
SESSION_MAKER = None

async def init_database():
    """Initializes the database connection and creates not-existing tables.
    """
    global ENGINE
    ENGINE = create_async_engine(f"postgresql+asyncpg://{config.POSTGIS_USER}:{config.POSTGIS_PASSWORD}@{config.POSTGIS_HOST}:{config.POSTGIS_PORT}/{config.POSTGIS_DB}")
    global SESSION_MAKER
    SESSION_MAKER = async_sessionmaker(bind=ENGINE, expire_on_commit=False)
    async with ENGINE.connect() as conn:
        await conn.run_sync(META_DATA.reflect)
        await conn.run_sync(META_DATA.create_all)
        await conn.commit()

async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    """Creates a new db session. Should be used as fastapi depends.
    """
    global SESSION_MAKER
    if SESSION_MAKER is None:
        raise ValueError("This should not have happened.")
    db = SESSION_MAKER()
    try:
        yield db
    finally:
        await db.close()
