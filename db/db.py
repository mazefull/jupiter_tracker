from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from models.data_models import Base

engine = create_async_engine(url=settings.DB_URL_ASYNC, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)

#
async def get_session():
    async with new_session() as session:
        yield session


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"success": True}
