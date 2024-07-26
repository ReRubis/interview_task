"""This module contains the schemas for music module."""

from enum import StrEnum

from pydantic import BaseModel


class MusicType(StrEnum):
    song = "Song"
    album = "Album"
    band = "Band"


class BandIn(BaseModel):
    name: str


class AlbumIn(BaseModel):
    name: str

    band_id: int


class SongIn(BaseModel):
    name: str

    album_id: int


class MusicIn(BaseModel):
    type: MusicType

    data: SongIn | AlbumIn | BandIn


class BandOut(BaseModel):
    id: int
    name: str


class AlbumOut(BaseModel):
    id: int
    name: str
    band_id: int


class SongOut(BaseModel):
    id: int
    name: str
    album_id: int


class MusicOut(BaseModel):
    type: MusicType

    data: list[BandOut | AlbumOut | SongOut]


class MusicUpdateIn(BaseModel):
    type: MusicType
    new_name: str
    music_id: int
