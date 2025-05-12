from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.repositories.user_repository import UserRepository
from app.auth.services.auth_service import AuthService
from app.auth.entities.user import UserCreate, UserLogin, Token
from app.auth.repositories.token_repository import TokenRepository
from app.auth.repositories.item_repository import ItemRepository


router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    user_repository = UserRepository(db)
    token_repository = TokenRepository(db)
    item_repository = ItemRepository(db)
    return AuthService(user_repository, token_repository, item_repository)


@router.post("/register", response_model=Token)
async def register(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    db_user = await auth_service.register_user(user)
    return await auth_service.create_tokens(db_user)


@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await auth_service.create_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.refresh_tokens(refresh_token)
