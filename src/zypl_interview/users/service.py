"""This module contains the service layer for the user module."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.auth.utils import verify_password
from src.zypl_interview.exceptions import CustomBaseError
from src.zypl_interview.users.repository import UserRepository
from src.zypl_interview.users.schemas import UserInAuth, UserInRegistration, UserOut

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def add_user(self, session: AsyncSession, user_in: UserInRegistration) -> int:
        logger.debug("Adding new user")

        return await self.user_repository.add_user(
            session, user_in.password, user_in.username, user_in.email
        )

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserOut:
        user = await self.user_repository.get_user_by_id(session, user_id)

        logger.debug("Getting user by id")

        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
        )

    async def change_username(
        self,
        session: AsyncSession,
        user_id: int,
        new_username: str,
    ) -> UserOut:
        logger.debug("Changing username")
        user = await self.user_repository.change_name(session, user_id, new_username)

        return UserOut(id=user.id, username=user.username, email=user.email)

    async def check_user(
        self,
        session: AsyncSession,
        user_in: UserInAuth,
    ) -> UserOut:
        """Checks if the user exists and if the password is correct."""

        user = await self.user_repository.get_user_by_email(session, user_in.email)

        if not user:
            raise CustomBaseError("Invalid credentials", status_code=401)

        if not verify_password(user_in.password, user.password):
            raise CustomBaseError("Invalid credentials", status_code=401)

        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
        )
