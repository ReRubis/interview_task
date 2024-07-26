import logging

from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.exceptions import CustomBaseError
from src.zypl_interview.users.models import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self): ...

    async def add_user(
        self, session: AsyncSession, password: str, username: str, email: str
    ) -> int:
        try:
            user = await session.execute(
                insert(
                    User,
                ).values(
                    password=password,
                    username=username,
                    email=email,
                ),
            )
            await session.commit()
            return user.inserted_primary_key[0]
        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise CustomBaseError("Registration Failed", 409) from e

    async def get_user_by_email(self, session: AsyncSession, email: str) -> User:
        try:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            raise CustomBaseError("User not found!", status_code=400) from e
        except AttributeError as e:
            logger.error(e)
            raise CustomBaseError("User not found!", status_code=400) from e

    async def get_user_by_id(self, session: AsyncSession, id: int) -> User:
        try:
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            raise CustomBaseError("User not found!", status_code=400) from e
        except AttributeError as e:
            logger.error(e)
            raise CustomBaseError("User not found!", status_code=400) from e

    async def change_name(
        self, session: AsyncSession, id: int, new_username: str
    ) -> User:
        try:
            stmt = (
                update(User)
                .where(User.id == id)
                .values(username=new_username)
                .returning(User)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(e)
            raise CustomBaseError("Login failed", status_code=400) from e
        except AttributeError as e:
            logger.error(e)
            raise CustomBaseError("Login failed", status_code=400) from e
