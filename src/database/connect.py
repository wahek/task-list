import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager

from src.config import settings
from src.database.models import metadata

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


if __name__ == '__main__':

    asyncio.run(create_tables())
