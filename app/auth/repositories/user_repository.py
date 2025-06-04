from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models.user import UserModel
from app.auth.entities.user import User, UserCreate, UserUpdate
from app.nutrition.models.restriction import RestrictionModel
from typing import Optional
from sqlalchemy.orm import selectinload


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return User.model_validate(user)
        return None
    

    async def get_by_email_new(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user


    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return User.from_orm(user)
        return None
    

    async def get_user(self, user_id: int) -> Optional[UserModel]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    
    async def get_user_gems(self, user_id: int) -> int:
        query = select(UserModel.gems).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.first()
        return user[0]


    async def create(self, user: UserCreate, hashed_password: str) -> User:
        db_user = UserModel(
            email=user.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == db_user.id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)


    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.restrictions), selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)


    async def add_gems_and_experience_blitz(self, user_id: int, gems: int = 0, expirience: int = 0) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.blitz_polls), selectinload(UserModel.restrictions), selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.gems = (db_user.gems or 0) + gems
        db_user.expirience = (db_user.expirience or 0) + expirience
        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.blitz_polls), selectinload(UserModel.restrictions), selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)
    

    async def add_injury_to_user(self, user: UserModel, muscle_groups) -> Optional[User]:
        for muscle_group in muscle_groups:
            if muscle_group not in user.injuries:
                user.injuries.append(muscle_group)

        await self.db.commit()
        await self.db.refresh(user)

        return User.from_orm(user)

    
    async def add_restrictions(self, user_id: int, restriction_ids: list[int]) -> User:
        query = select(UserModel).options(
            selectinload(UserModel.restrictions),
            selectinload(UserModel.injuries)
        ).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Пользователь с ID {user_id} не найден"
        #     )
        
        # Получаем все ограничения, которые нужно добавить
        restriction_query = select(RestrictionModel).where(
            RestrictionModel.id.in_(restriction_ids)
        )
        result = await self.db.execute(restriction_query)
        restrictions = result.scalars().all()
        
        # Добавляем новые ограничения к существующим
        existing_ids = {r.id for r in user.restrictions}
        for restriction in restrictions:
            if restriction.id not in existing_ids:
                user.restrictions.append(restriction)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        # Загружаем обновленного пользователя с ограничениями
        query = select(UserModel).options(
            selectinload(UserModel.restrictions)
        ).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        updated_user = result.scalar_one_or_none()
        
        return User.model_validate(updated_user)


    async def add_gems_and_experience(self, user_id: int, gems: int = 0, expirience: int = 0) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.gems = (db_user.gems or 0) + gems
        db_user.expirience = (db_user.expirience or 0) + expirience
        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.restrictions)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)
    

    async def increase_burned_calories(self, user_id: int, burned_calories: int) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.calories_burned_daily = (db_user.calories_burned_daily or 0) + burned_calories
        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.restrictions), selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)
    

    async def increase_calories(self, user_id: int, calories: float, proteins: float,
                                fats: float, carbs: float) -> Optional[User]:
        query = select(UserModel).options(selectinload(UserModel.restrictions),
                                          selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        db_user.calories_eaten_daily = (db_user.calories_eaten_daily or 0) + calories
        db_user.proteins_eaten_daily = (db_user.proteins_eaten_daily or 0) + proteins
        db_user.fats_eaten_daily = (db_user.fats_eaten_daily or 0) + fats
        db_user.carbs_eaten_daily = (db_user.carbs_eaten_daily or 0) + carbs
        await self.db.commit()
        await self.db.refresh(db_user)
        
        query = select(UserModel).options(selectinload(UserModel.restrictions), selectinload(UserModel.injuries)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        refreshed_user = result.scalar_one_or_none()
        
        return User.model_validate(refreshed_user)
