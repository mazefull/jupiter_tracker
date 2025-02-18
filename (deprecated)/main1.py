from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from pydantic import BaseModel, Field, ConfigDict
import asyncpg
from typing import Annotated, Optional
from src.db.dataclasses import *


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

app = FastAPI()
engine = create_async_engine(f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')
# engine = create_async_engine('postgresql+asyncpg://postgres:mazefull1@localhost:5432/postgres')
new_session = async_sessionmaker(engine, expire_on_commit=False)



async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/tasks/setup_db", summary='HARD RESET DB')
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"successs": True}



@app.get("/tasks/{task_id}")
async def get_task_data(task_id: str, session: SessionDep):
    query = select(SRTask).where(SRTask.task_id == task_id)
    data = await session.execute(query)
    return data.scalars().first()


@app.get("/tasks/{task_id}/comments")
async def get_task_comments(task_id: str, session: SessionDep):
    query_ids = select(SRActions.comment_id).where(SRActions.task_id == task_id)
    comments_ids = await session.execute(query_ids)

    query_comments = select(SRComment).where(SRComment.comment_id == comments_ids.scalars().all())
    comments_data = await session.execute(query_comments)
    return comments_data.scalars().all()


@app.get("/tasks/{task_id}/assignments")
async def get_task_assignments(task_id: str, session: SessionDep):
    query_ids = select(SRActions.assignment_id).where(SRTask.task_id == task_id)
    assignments_ids = await session.execute(query_ids)

    query_assignments = select(SRAssignment).where(SRAssignment.assignment_id == assignments_ids.scalars().all())
    assignments_data = await session.execute(query_assignments)
    return assignments_data


@app.get("/tasks/{task_id}/statuses")
async def get_task_statuses(task_id: str, session: SessionDep):
    query_ids = select(SRActions.status_id).where(SRTask.task_id == task_id)
    statuses_ids = await session.execute(query_ids)

    query_statuses = select(SRStatus).where(SRStatus.status_id == statuses_ids.scalars().all())
    status_data = await session.execute(query_statuses)
    return status_data.scalars().all()