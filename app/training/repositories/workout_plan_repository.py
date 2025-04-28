from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.training.models.workout_plan import WorkoutPlanModel


class WorkoutPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_id(self, workout_plan_id: int) -> WorkoutPlanModel | None:
        query = select(WorkoutPlanModel).where(WorkoutPlanModel.id == workout_plan_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def create(self, workout_plan: WorkoutPlanModel) -> WorkoutPlanModel:
        self.db.add(workout_plan)
        await self.db.commit()
        await self.db.refresh(workout_plan)
        return workout_plan


    async def update(self, workout_plan_id: int, update_data: dict) -> WorkoutPlanModel | None:
        query = update(WorkoutPlanModel).where(WorkoutPlanModel.id == workout_plan_id).values(**update_data)
        result = await self.db.execute(query)
        if result.rowcount == 0:
            return None
        await self.db.commit()
        return await self.get_by_id(workout_plan_id)


    async def delete(self, workout_plan_id: int) -> None:
        query = delete(WorkoutPlanModel).where(WorkoutPlanModel.id == workout_plan_id)
        await self.db.execute(query)
        await self.db.commit()


    async def   get_by_user_id(self, user_id: int) -> list[WorkoutPlanModel] | None:
        query = select(WorkoutPlanModel).where(WorkoutPlanModel.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
