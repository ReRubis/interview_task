"""This module contains the business logic, service layer for the subscriptions module."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.integration.email import EmailIntegration
from src.zypl_interview.subscriptions.repository import SubscriptionRepository
from src.zypl_interview.subscriptions.schemas import SubscriptionIn

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Service class for the subscriptions module."""

    def __init__(
        self,
        subscription_repo: SubscriptionRepository,
        email_integration: EmailIntegration,
    ) -> None:
        self.subscription_repo = subscription_repo
        self.email_integration = email_integration

    async def subscribe_to_band(
        self, session: AsyncSession, user_email: int, album: SubscriptionIn
    ) -> dict[str, str]:
        """Subscribes a user to new album releases of the band."""
        logger.debug("Subscribing user to band")

        result = await self.subscription_repo.insert_subscription(
            session, user_email, album.band_id
        )

        return {
            "message": f"User subscribed to band {result.band_id}",
        }

    async def check_subscriptions(
        self, session: AsyncSession, band_id: int, album_id: int
    ) -> None:
        """Check a user's subscriptions."""
        logger.debug("Checking user subscriptions")

        subscriptions = await self.subscription_repo.get_subscriptions_by_band_id(
            session, band_id
        )

        for sub in subscriptions:
            logger.debug(
                f"User {sub.user_email} is being notified about new album {album_id} from {sub.band_id}"
            )

            await self.email_integration.send_email(
                sub.user_email,
                f"New album {album_id} from {sub.band_id}",
                f"New album {album_id} from {sub.band_id}",
            )
