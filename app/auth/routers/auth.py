from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.repositories.user_repository import UserRepository
from auth.services.auth_service import AuthService
from auth.entities.user import UserCreate, UserLogin, Token


router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)


@router.post("/register", response_model=Token)
async def register(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    db_user = await auth_service.register_user(user)
    return auth_service.create_tokens(db_user)


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
    return auth_service.create_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    token_data = await auth_service.verify_token(token)
    user = await auth_service.user_repository.get_by_email(token_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_tokens(user)
