from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.auth.jwt import Credentials, JWTBearer
from src.zypl_interview.database import get_db_session
from src.zypl_interview.music.injectors import get_music_service
from src.zypl_interview.music.schemas import MusicIn, MusicOut, MusicType, MusicUpdateIn
from src.zypl_interview.music.service import MusicService

router = APIRouter(prefix="/music", tags=["music"])


@router.post("/", response_model=MusicOut)
async def add_music(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    music: MusicIn,
    music_service: Annotated[MusicService, Depends(get_music_service)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
) -> MusicOut:
    """Add a new music.

    Takes in a music object and adds it to the database.
    """
    return await music_service.add_music(
        session,
        music,
    )


@router.get("/", response_model=MusicOut)
async def get_music(
    music_type: MusicType,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    music_service: Annotated[MusicService, Depends(get_music_service)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
) -> MusicOut:
    """Get all music objects.

    Returns all music objects in the database.
    """
    return await music_service.get_music(session, music_type)


@router.patch("/", response_model=MusicOut)
async def update_music(
    update_data: MusicUpdateIn,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    music_service: Annotated[MusicService, Depends(get_music_service)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
) -> MusicOut:
    """Update a music object.

    Takes in a music object and updates it in the database.
    """
    return await music_service.update_music(
        session=session,
        music_type=update_data.type,
        music_id=update_data.music_id,
        new_name=update_data.new_name,
    )


@router.delete("/")
async def delete_music(
    music_id: int,
    music_type: MusicType,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    music_service: Annotated[MusicService, Depends(get_music_service)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
) -> dict[str, str]:
    """Delete a music object.

    Takes in a music object id and deletes it from the database.
    """
    return await music_service.delete_music(
        session=session,
        music_type=music_type,
        music_id=music_id,
    )


@router.post("/csv_upload")
async def upload_csv(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    music_service: Annotated[MusicService, Depends(get_music_service)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
    file: Annotated[UploadFile, File(description=".csv")] = None,
) -> dict[str, str]:
    """Upload music data from a csv file.

    Takes in a csv file and uploads the data to the database.
    """
    return await music_service.insert_songs_from_csv_file(session, file)
