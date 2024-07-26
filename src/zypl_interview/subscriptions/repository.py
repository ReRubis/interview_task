"""This module contains the sql logic for the subscriptions module."""

import logging

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.exceptions import CustomBaseError
from src.zypl_interview.subscriptions.models import Subscription

logger = logging.getLogger(__name__)


class SubscriptionRepository:
    def __init__(self) -> None: ...

    async def insert_subscription(
        self,
        session: AsyncSession,
        user_email: str,
        band_id: int,
    ) -> Subscription:
        stmt = (
            insert(
                Subscription,
            )
            .values(
                user_email=user_email,
                band_id=band_id,
            )
            .returning(Subscription)
        )
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Failed to insert subscription", 500) from e

    async def get_subscriptions_by_band_id(
        self,
        session: AsyncSession,
        band_id: int,
    ) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.band_id == band_id)
        try:
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(e)
            raise CustomBaseError("Failed to get subscriptions", 500) from e
