# database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

# 1. Base class for models
Base = declarative_base()

# 2. Async database URL (SQLite with aiosqlite or PostgreSQL with asyncpg)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# Example PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# 3. Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# 4. Create async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 5. Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
