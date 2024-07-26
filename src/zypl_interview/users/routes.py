"""This module contains the routes for the user module."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.zypl_interview.auth.jwt import Credentials, JWTAuth, JWTBearer
from src.zypl_interview.auth.schemas import TokenOut
from src.zypl_interview.database import get_db_session
from src.zypl_interview.users.injectors import get_user_service
from src.zypl_interview.users.schemas import UserInAuth, UserInRegistration, UserOut
from src.zypl_interview.users.service import UserService

router = APIRouter(prefix="/users")


@router.post(
    "/register/",
    tags=["users"],
    response_model=TokenOut,
)
async def register(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: UserInRegistration,
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_auth: Annotated[JWTAuth, Depends(JWTAuth)],
) -> TokenOut:
    """Register a new user.

    User is associated with email.
    """
    user_id = await user_service.add_user(
        session,
        user,
    )
    user = await user_service.get_user_by_id(session, user_id)

    access_token = jwt_auth.generate_access_token(user)

    return TokenOut(
        access_token=access_token,
    )


@router.post(
    "/login/",
    tags=["users"],
    response_model=TokenOut,
)
async def login(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: UserInAuth,
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_auth: Annotated[JWTAuth, Depends(JWTAuth)],
) -> TokenOut:
    """Register a new user.

    User is associated with email.
    """

    user = await user_service.check_user(session, user)
    access_token = jwt_auth.generate_access_token(user)

    return TokenOut(
        access_token=access_token,
    )


@router.get(
    "/me/",
    tags=["users"],
    response_model=UserOut,
)
async def get_me(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    credentials: Annotated[Credentials, Depends(JWTBearer())],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserOut:
    return await user_service.get_user_by_id(
        session,
        credentials.user.id,
    )


@router.patch(
    "/username/",
    tags=["users"],
    response_model=UserOut,
)
async def change_username(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    username: str,
    credentials: Annotated[Credentials, Depends(JWTBearer())],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserOut:
    """Change user's username."""
    return await user_service.change_username(
        session,
        user_id=credentials.user.id,
        new_username=username,
    )
