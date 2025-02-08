from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.data_models import Base

# from main import settings

engine = create_async_engine('')
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"success": True}
