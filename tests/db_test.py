import sys
import os
from contextlib import asynccontextmanager

from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import settings
from src.database.models import metadata, Task

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True, )
SessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
@pytest.fixture(scope='session')
async def async_db() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
async def init_task(async_db: AsyncSession) -> Task:
    return Task(title="test", description="test")


pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_create_task(async_db: AsyncSession, init_task: Task):
    async with async_db as db:
        db.add(await init_task)
        await db.commit()
        assert init_task.id == db.query(init_task).first().id
