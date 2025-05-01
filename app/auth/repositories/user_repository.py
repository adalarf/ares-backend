from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models.user import UserModel
from app.auth.entities.user import User, UserCreate, UserUpdate
from typing import Optional
from sqlalchemy.orm import selectinload


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions)).where(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return User.model_validate(user)
        return None


    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return User.model_validate(user)
        return None


    async def create(self, user: UserCreate, hashed_password: str) -> User:
        db_user = UserModel(
            email=user.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return User.from_orm(db_user)


    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return User.from_orm(db_user)


    async def add_gems_and_experience_blitz(self, user_id: int, gems: int = 0, expirience: int = 0) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.blitz_polls), selectinload(UserModel.restrictions)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.gems = (db_user.gems or 0) + gems
        db_user.expirience = (db_user.expirience or 0) + expirience
        await self.db.commit()
        await self.db.refresh(db_user)
        return User.from_orm(db_user)
    

    async def add_gems_and_experience(self, user_id: int, gems: int = 0, expirience: int = 0) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.gems = (db_user.gems or 0) + gems
        db_user.expirience = (db_user.expirience or 0) + expirience
        await self.db.commit()
        await self.db.refresh(db_user)
