from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

async_engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,  # type: ignore
)
