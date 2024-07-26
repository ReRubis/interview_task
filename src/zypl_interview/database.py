"""This module contains the database configuration."""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.zypl_interview.config import config

DB_URL = URL.create(
    drivername=config.DB_DRIVER,
    username=config.DB_USERNAME,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME,
)

engine = create_async_engine(
    DB_URL,
    # echo=config.DB_ECHO,
)


async def get_db_session() -> AsyncSession:
    """Get the database session."""
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            yield session
            await session.commit()
            await asyncio.shield(session.close())

        except Exception:
            await session.rollback()
            raise
        finally:
            await asyncio.shield(session.close())


@asynccontextmanager
async def get_db_context_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database session."""
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            yield session
            await session.commit()
            await asyncio.shield(session.close())

        except Exception:
            await session.rollback()
            raise
        finally:
            await asyncio.shield(session.close())


class Base(DeclarativeBase):
    """Base class for the database models."""

    pass  # noqa: PIE790
