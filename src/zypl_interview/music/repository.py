import logging
from typing import Type

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.exceptions import CustomBaseError
from src.zypl_interview.music.models import Album, Band, Song

logger = logging.getLogger(__name__)


class MusicRepository:
    def __init__(self): ...

    async def add_song(self, session: AsyncSession, name: str, album_id: str) -> Song:
        stmt = (
            insert(
                Song,
            )
            .values(
                album_id=album_id,
                name=name,
            )
            .returning(Song)
        )
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Failed to insert song", 409) from e

    async def add_album(self, session: AsyncSession, name: str, band_id: str) -> Album:
        stmt = insert(Album).values(name=name, band_id=band_id).returning(Album)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Insertion failed", 409) from e

    async def add_band(self, session: AsyncSession, name: str) -> Band:
        stmt = insert(Band).values(name=name).returning(Band)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Insertion failed", 409) from e

    async def get_music(
        self,
        session: AsyncSession,
        music: Type[Song] | Type[Album] | Type[Band],
    ) -> list[Song | Album | Band]:
        stmt = select(music).limit(10)
        try:
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(e)
            raise CustomBaseError("Music not found!", status_code=400) from e
        except AttributeError as e:
            logger.error(e)
            raise CustomBaseError("Music not found!", status_code=400) from e

    async def update_music(
        self,
        session: AsyncSession,
        music: Type[Song] | Type[Album] | Type[Band],
        music_id: int,
        new_name: str,
    ) -> list[Song | Album | Band]:
        stmt = (
            update(music)
            .where(music.id == music_id)
            .values(name=new_name)
            .returning(music)
        )
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Update failed", status_code=400) from e

    async def delete_music(
        self,
        session: AsyncSession,
        music: Type[Song] | Type[Album] | Type[Band],
        music_id: int,
    ) -> None:
        stmt = delete(music).where(music.id == music_id)
        try:
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Deletion failed", status_code=400) from e
