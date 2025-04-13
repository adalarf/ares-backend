from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.training.models.planned_exercise import PlannedExerciseModel


class PlannedExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    

    async def get_by_id(self, planned_exercise_id: int) -> PlannedExerciseModel | None:
        query = select(PlannedExerciseModel).where(PlannedExerciseModel.id == planned_exercise_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    

    async def create(self, planned_exercise: PlannedExerciseModel) -> PlannedExerciseModel: 
        self.db.add(planned_exercise)
        await self.db.commit()
        await self.db.refresh(planned_exercise)
        return planned_exercise
    

    async def update(self, planned_exercise_id: int, update_data: dict) -> PlannedExerciseModel | None:     
        query = update(PlannedExerciseModel).where(PlannedExerciseModel.id == planned_exercise_id).values(**update_data)
        result = await self.db.execute(query)
        if result.rowcount == 0:
            return None
        await self.db.commit()
        return await self.get_by_id(planned_exercise_id)
    

    async def delete(self, planned_exercise_id: int) -> None:
        query = delete(PlannedExerciseModel).where(PlannedExerciseModel.id == planned_exercise_id)
        await self.db.execute(query)
        await self.db.commit()

    
    async def get_by_workout_day_id(self, workout_day_id: int) -> list[PlannedExerciseModel]:
        query = select(PlannedExerciseModel).where(PlannedExerciseModel.workout_day_id == workout_day_id)
        result = await self.db.execute(query)
        return result.scalars().all()
