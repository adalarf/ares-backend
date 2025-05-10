from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.repositories.user_repository import UserRepository
from app.auth.repositories.token_repository import TokenRepository
from app.auth.services.auth_service import AuthService
from app.auth.entities.user import User, UserUpdate, UserInfo, CaloriesInfo
from app.auth.services.auth_service import get_current_user

router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    user_repository = UserRepository(db)
    token_repository = TokenRepository(db)
    return AuthService(user_repository, token_repository)


@router.patch("/stats", response_model=User)
async def update_user_stats(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.update_user_stats(current_user.id, user_update)


@router.get("/info", response_model=UserInfo)
async def get_user_info(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    user_info = await auth_service.get_user_info(current_user.id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_info


@router.get("/get_calories_info", response_model=CaloriesInfo)
async def get_calories_info(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    body_mass_index = await auth_service.get_body_mass_index(current_user.weight, current_user.height)
    if not body_mass_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calories info not found")
    return CaloriesInfo(body_mass_index=body_mass_index)
