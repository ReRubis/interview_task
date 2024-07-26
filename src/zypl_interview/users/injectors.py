from src.zypl_interview.users.repository import UserRepository
from src.zypl_interview.users.service import UserService


async def get_user_service() -> UserService:
    """Get UserService instance."""
    user_repository = UserRepository()
    return UserService(
        user_repository=user_repository,
    )
