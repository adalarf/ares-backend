from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.training.models.random_exercise import RandomExerciseModel
from app.training.entities.random_exercise import RandomExerciseCreation


class RandomExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, random_exercise: RandomExerciseCreation) -> RandomExerciseModel:
        random_exercise_model = RandomExerciseModel(
            sets_number=random_exercise.sets_number,
            repetitions=random_exercise.repetitions,
            gems=random_exercise.gems,
            expirience=random_exercise.expirience,
            exercise_id=random_exercise.exercise_id,
            user_id=random_exercise.user_id,
            calories=random_exercise.calories
        )
        self.db.add(random_exercise_model)
        await self.db.commit()
        await self.db.refresh(random_exercise_model)
        return random_exercise_model


    async def get_by_user_id(self, user_id: int) -> list[RandomExerciseModel]:
        query = select(RandomExerciseModel).options(selectinload(RandomExerciseModel.exercise)).where(RandomExerciseModel.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_id(self, random_exercise_id: int) -> RandomExerciseModel:
        query = select(RandomExerciseModel).where(RandomExerciseModel.id == random_exercise_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def delete(self, random_exercise_id: int) -> None:
        query = select(RandomExerciseModel).where(RandomExerciseModel.id == random_exercise_id)
        result = await self.db.execute(query)
        random_exercise = result.scalar_one_or_none()
        if random_exercise:
            await self.db.delete(random_exercise)
            await self.db.commit()
        