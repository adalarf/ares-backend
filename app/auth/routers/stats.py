from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.repositories.user_repository import UserRepository
from app.auth.repositories.token_repository import TokenRepository
from app.auth.repositories.item_repository import ItemRepository
from app.auth.services.auth_service import AuthService
from app.auth.entities.user import User, UserUpdate, UserInfo, CaloriesInfo, AvatarUrl
from app.auth.entities.item import ItemId, ItemsInfo, ItemInfo
from app.auth.services.auth_service import get_current_user

router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    user_repository = UserRepository(db)
    token_repository = TokenRepository(db)
    item_repository = ItemRepository(db)
    return AuthService(user_repository, token_repository, item_repository)


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


@router.post("/set_avatar")
async def set_user_avatar(
    avatar_url: AvatarUrl,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    
    result = await auth_service.set_user_avatar(current_user, avatar_url.avatar_url)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"message": "Avatar updated successfully"}


@router.get("/get_user_avatar")
async def get_user_avatar(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    user_avatar = await auth_service.get_user_avatar(current_user.id)
    if not user_avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")
    return {"avatar": user_avatar}


@router.post("/buy_items")
async def buy_clothes(
    item_id: ItemId,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    result = await auth_service.buy_clothes(current_user.id, item_id.id)
    return result


@router.get("/get_items", response_model=ItemsInfo)
async def get_user_items(
    auth_service: AuthService = Depends(get_auth_service)
):
    user_items = await auth_service.get_items()
    if not user_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Items not found")
    user_items = []
    for user_item in user_items:
        item = ItemInfo(
            id=user_item.id,
            name=user_item.name,
            description=user_item.description,
            price=user_item.price,
            path=user_item.path
        )
        user_items.append(item)
    user_items = ItemsInfo(items=user_items)
    return user_items


@router.get("/get_user_items", response_model=ItemsInfo)
async def get_user_items(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    user_items_db = await auth_service.get_user_items(current_user.id)
    if not user_items_db:
        return ItemsInfo(items=[])
    
    items_list = []
    for item in user_items_db:
        items_list.append(ItemInfo(
            id=item.id,
            name=item.name,
            path=item.path or "",
            price=int(item.price),
            rarity=item.rarity or ""
        ))
    
    return ItemsInfo(items=items_list)