from src.zypl_interview.integration.email import EmailIntegration
from src.zypl_interview.subscriptions.repository import SubscriptionRepository
from src.zypl_interview.subscriptions.service import SubscriptionService


async def get_subs_service() -> SubscriptionService:
    """Get SubscriptionService instance."""
    sub_repo = SubscriptionRepository()
    email_integ = EmailIntegration()
    return SubscriptionService(
        subscription_repo=sub_repo, email_integration=email_integ
    )
