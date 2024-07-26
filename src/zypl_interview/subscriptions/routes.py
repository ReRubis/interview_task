"""This module contains the routes for the subscriptions module."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.auth.jwt import Credentials, JWTBearer
from src.zypl_interview.database import get_db_session
from src.zypl_interview.subscriptions.injectors import get_subs_service
from src.zypl_interview.subscriptions.schemas import SubscriptionIn
from src.zypl_interview.subscriptions.service import SubscriptionService

router = APIRouter(prefix="/subscriptions")


@router.post(
    "/subscribe/",
)
async def subscribe(
    album: SubscriptionIn,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
    subscription_service: Annotated[SubscriptionService, Depends(get_subs_service)],
) -> dict[str, str]:
    """Subscribes a user to new album releases of the band."""

    return await subscription_service.subscribe_to_band(
        session, credentials.user.email, album
    )
