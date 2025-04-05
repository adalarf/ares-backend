from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from .database import async_session_maker
from app.auth.repositories.token_repository import TokenRepository
from .config import ACCESS_TOKEN_EXPIRE_MINUTES


async def cleanup_expired_tokens():
    async with async_session_maker() as session:
        token_repository = TokenRepository(session)
        await token_repository.cleanup_expired_tokens()


def setup_periodic_tasks(app: FastAPI):
    @app.on_event("startup")
    @repeat_every(seconds=60 * int(ACCESS_TOKEN_EXPIRE_MINUTES))
    async def cleanup_tokens_task():
        await cleanup_expired_tokens() 