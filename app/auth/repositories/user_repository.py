from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models.user import UserModel
from auth.entities.user import User, UserCreate
from typing import Optional


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
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
