from fastapi import APIRouter

from src.zypl_interview.music.routes import router as music_router
from src.zypl_interview.subscriptions.routes import router as subscription_router
from src.zypl_interview.users.routes import router as user_router


def router_factory() -> APIRouter:
    """Creates the router for the FastAPI app."""
    router = APIRouter(
        prefix="/api",
    )
    router.include_router(user_router)
    router.include_router(subscription_router)
    router.include_router(music_router)

    return router
