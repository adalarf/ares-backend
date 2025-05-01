from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.training.models.planned_exercise import PlannedExerciseModel
from app.training.entities.planned_exercise import PlannedExerciseCreation


class PlannedExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    

    async def get_by_id(self, planned_exercise_id: int) -> PlannedExerciseModel | None:
        query = select(PlannedExerciseModel).where(PlannedExerciseModel.id == planned_exercise_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    

    async def create(self, planned_exercise: PlannedExerciseCreation) -> PlannedExerciseModel:
        planned_exercise_model = PlannedExerciseModel(
            workout_day_id=planned_exercise.workout_day_id,
            exercise_id=planned_exercise.exercise_id,
            sets_number=planned_exercise.sets_number,
            repetitions=planned_exercise.repetitions,
            gems=planned_exercise.gems,
            expirience=planned_exercise.expirience
        )
        self.db.add(planned_exercise_model)
        await self.db.commit()
        await self.db.refresh(planned_exercise_model)
        return planned_exercise_model
    

    async def update(self, planned_exercise_id: int):     
        query = (
            update(PlannedExerciseModel)
            .where(PlannedExerciseModel.id == planned_exercise_id)
            .values(is_active=False)
        )
        await self.db.execute(query)
        await self.db.commit()
    

    async def delete(self, planned_exercise_id: int) -> None:
        query = delete(PlannedExerciseModel).where(PlannedExerciseModel.id == planned_exercise_id)
        await self.db.execute(query)
        await self.db.commit()

    
    async def get_by_workout_day_id(self, workout_day_id: int) -> list[PlannedExerciseModel]:
        query = (
            select(PlannedExerciseModel)
            .options(selectinload(PlannedExerciseModel.exercise))
            .where(PlannedExerciseModel.workout_day_id == workout_day_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
