import logging
import uuid
from datetime import datetime
from typing import Any

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from src.zypl_interview.auth.schemas import DecodedToken
from src.zypl_interview.config import config
from src.zypl_interview.database import get_db_context_session
from src.zypl_interview.users.repository import UserRepository
from src.zypl_interview.users.schemas import UserOut
from src.zypl_interview.users.service import UserService

logger = logging.getLogger(__name__)


class Credentials(BaseModel):
    """Authenticated user model."""

    token: DecodedToken

    user: UserOut


class JWTAuth:
    def _generate_token(
        self,
        type: str,
        subject: str,
        payload: dict[str, Any],
    ) -> str:
        current_timestamp = datetime.now().timestamp()

        data = dict(
            iss="zypl",
            sub=subject,
            type=type,
            jti=str(uuid.uuid4()),
            iat=int(current_timestamp),
            nbf=int(current_timestamp),
        )
        payload.update(data)

        logger.debug("Generating JWT. Payload:", extra=payload)

        return jwt.encode(
            payload=payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
        )

    def generate_access_token(self, user_in: UserOut) -> str:
        return self._generate_token(
            "access",
            user_in.id,
            {"id": user_in.id},
        )

    @staticmethod
    def decode_jwt(token: str) -> DecodedToken | None:
        try:
            decoded_token = jwt.decode(
                token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
            return DecodedToken(**decoded_token)
        except Exception as e:
            logging.error(e)
            return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Credentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            token = self.verify_jwt(credentials.credentials)
            if not token:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            async with get_db_context_session() as session:
                user_service = UserService(
                    UserRepository(),
                )
                logger.debug("Getting user by id")
                user = await user_service.get_user_by_id(session, token.id)

                return Credentials(user=user, token=token)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> DecodedToken | None:
        try:
            payload = JWTAuth.decode_jwt(jwtoken)
            return payload
        except Exception:
            return None
