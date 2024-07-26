"""This module contains the service layer for the music module."""

import csv
import logging
from typing import Type

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.music.models import Album, Band, Song
from src.zypl_interview.music.repository import MusicRepository
from src.zypl_interview.music.schemas import (
    AlbumOut,
    BandOut,
    MusicIn,
    MusicOut,
    MusicType,
    SongOut,
)
from src.zypl_interview.subscriptions.service import SubscriptionService

logger = logging.getLogger(__name__)


class MusicService:
    def __init__(
        self,
        music_repository: MusicRepository,
        subscription_service: SubscriptionService,
    ) -> None:
        self.mus_repository = music_repository
        self.subscription_service = subscription_service

    async def add_music(self, session: AsyncSession, music: MusicIn) -> MusicOut:
        """Add a new music object to db."""
        logger.debug(f"Adding new music {type(music.data)}")

        if music.type == MusicType.band:
            result = await self.mus_repository.add_band(
                session,
                music.data.name,
            )
            return MusicOut(
                type=MusicType.band,
                data=[
                    BandOut(
                        id=result.id,
                        name=result.name,
                    )
                ],
            )

        if music.type == MusicType.album:
            result = await self.mus_repository.add_album(
                session,
                music.data.name,
                music.data.band_id,
            )
            await self.subscription_service.check_subscriptions(
                session, result.band_id, result.id
            )
            return MusicOut(
                type=MusicType.album,
                data=[
                    AlbumOut(
                        id=result.id,
                        name=result.name,
                        band_id=result.band_id,
                    )
                ],
            )

        if music.type == MusicType.song:
            result = await self.mus_repository.add_song(
                session,
                music.data.name,
                music.data.album_id,
            )
            return MusicOut(
                type=MusicType.song,
                data=[
                    SongOut(
                        id=result.id,
                        name=result.name,
                        album_id=result.album_id,
                    )
                ],
            )

        raise HTTPException(status_code=422, detail="Wrong input data")

    async def get_music(self, session: AsyncSession, music_type: MusicType) -> MusicOut:
        """Get music objects from db."""

        referense_type = await self._return_music_type(music_type)

        music = await self.mus_repository.get_music(session, referense_type)

        logger.debug("Getting music by id")

        if music is None:
            raise HTTPException(status_code=404, detail="Music not found")

        data = await self._format_output_data(music)

        return MusicOut(type=music_type, data=data)

    async def update_music(
        self, session: AsyncSession, music_type: MusicType, music_id: int, new_name: str
    ) -> MusicOut:
        reference_type = await self._return_music_type(music_type)

        music = await self.mus_repository.update_music(
            session, reference_type, music_id, new_name
        )

        if not music:
            raise HTTPException(status_code=404, detail="Music not found")

        data = await self._format_output_data(music)

        logger.debug("Updating music")

        return MusicOut(
            type=music_type,
            data=data,
        )

    async def delete_music(
        self, session: AsyncSession, music_type: MusicType, music_id: int
    ) -> dict[str, str]:
        reference_type = await self._return_music_type(music_type)

        await self.mus_repository.delete_music(session, reference_type, music_id)

        logger.debug("Deleting music")

        return {"message": "Music object deleted successfully"}

    async def insert_songs_from_csv_file(
        self,
        session: AsyncSession,
        file: UploadFile,
    ) -> str:
        """Make sure that albums with such ID exist before inserting."""
        if file.content_type != "text/csv":
            raise HTTPException(status_code=422, detail="Wrong file format")

        content = await file.read()
        content = content.decode("utf-8").splitlines()

        csv_reader = csv.reader(content)
        next(csv_reader)

        for row in csv_reader:
            song_name = row[1]
            album_id = int(row[0])
            logger.debug('Adding song "%s" to album with id %s', song_name, album_id)
            await self.mus_repository.add_song(session, song_name, album_id)
        return {"message": "Songs added successfully"}

    @classmethod
    async def _return_music_type(cls, type: MusicType) -> Type[Song | Album | Band]:
        if type == MusicType.band:
            return Band
        elif type == MusicType.album:
            return Album
        elif type == MusicType.song:
            return Song
        else:
            raise HTTPException(status_code=422, detail="Wrong input data")

    @classmethod
    async def _format_output_data(
        cls,
        music: list[Band | Album | Song],
    ) -> list[BandOut | AlbumOut | SongOut]:
        data = []
        if type(music[0]) is Band:
            for band in music:
                data.append(
                    BandOut(
                        id=band.id,
                        name=band.name,
                    )
                )
        elif type(music[0]) is Album:
            for album in music:
                data.append(
                    AlbumOut(
                        id=album.id,
                        name=album.name,
                        band_id=album.band_id,
                    )
                )
        elif type(music[0]) is Song:
            for song in music:
                data.append(
                    SongOut(
                        id=song.id,
                        name=song.name,
                        album_id=song.album_id,
                    )
                )
        else:
            raise HTTPException(status_code=404, detail="Music not found")
        return data
