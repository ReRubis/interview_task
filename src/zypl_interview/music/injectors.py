"""This module contains injector of music service."""

from src.zypl_interview.music.repository import MusicRepository
from src.zypl_interview.music.service import MusicService
from src.zypl_interview.subscriptions.injectors import get_subs_service


async def get_music_service() -> MusicService:
    """Get MusicService instance."""
    music_repository = MusicRepository()
    subscription_service = await get_subs_service()
    return MusicService(
        subscription_service=subscription_service,
        music_repository=music_repository,
    )
