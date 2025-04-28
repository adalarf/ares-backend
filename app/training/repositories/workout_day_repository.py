from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.training.models.workout_day import WorkoutDayModel
from sqlalchemy.orm import selectinload
from app.training.models.planned_exercise import PlannedExerciseModel


class WorkoutDayRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_id(self, workout_day_id: int) -> WorkoutDayModel | None:
        query = select(WorkoutDayModel).where(WorkoutDayModel.id == workout_day_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def create(self, workout_day: WorkoutDayModel) -> WorkoutDayModel:
        self.db.add(workout_day)
        await self.db.commit()
        await self.db.refresh(workout_day)
        return workout_day


    async def update(self, workout_day_id: int, update_data: dict) -> WorkoutDayModel | None:
        query = update(WorkoutDayModel).where(WorkoutDayModel.id == workout_day_id).values(**update_data)
        result = await self.db.execute(query)
        if result.rowcount == 0:
            return None
        await self.db.commit()
        return await self.get_by_id(workout_day_id)


    async def delete(self, workout_day_id: int) -> None:
        query = delete(WorkoutDayModel).where(WorkoutDayModel.id == workout_day_id)
        await self.db.execute(query)
        await self.db.commit()

    async def get_by_workout_plan_id(self, workout_plan_id: int) -> list[WorkoutDayModel]:
        query = (
            select(WorkoutDayModel)
            .options(selectinload(WorkoutDayModel.muscle_group))
            .where(WorkoutDayModel.workout_plan_id == workout_plan_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def deactivate_workout_day(self, workout_day_id: int):
        query = (
            update(WorkoutDayModel)
            .where(WorkoutDayModel.id == workout_day_id)
            .values(is_active=False)
        )
        await self.db.execute(query)
        await self.db.commit()

    async def has_active_planned_exercise(self, workout_day_id: int) -> bool:
        query = (
            select(PlannedExerciseModel)
            .where(
                PlannedExerciseModel.workout_day_id == workout_day_id,
                PlannedExerciseModel.is_active == True
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
