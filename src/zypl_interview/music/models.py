from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.zypl_interview.database import Base


class Band(Base):
    __tablename__ = "bands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    band_id: Mapped[int] = mapped_column(ForeignKey(Band.id), nullable=False)


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    album_id: Mapped[int] = mapped_column(ForeignKey(Album.id), nullable=False)
