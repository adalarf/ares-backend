from sqlalchemy import select
from app.training.models.muscle_group import MuscleGroupModel
from app.training.models.exercise import ExerciseModel
from sqlalchemy.ext.asyncio import AsyncSession


class MuscleGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_name(self, name: str) -> MuscleGroupModel | None:
        query = select(MuscleGroupModel).where(MuscleGroupModel.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def create(self, name: str) -> MuscleGroupModel:
        muscle_group = MuscleGroupModel(name=name)
        self.db.add(muscle_group)
        await self.db.commit()
        await self.db.refresh(muscle_group)
        return muscle_group


    async def get_all(self) -> list[MuscleGroupModel]:
        query = select(MuscleGroupModel)
        result = await self.db.execute(query)
        return result.scalars().all()


class ExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_muscle_group_and_place(self, muscle_group_id: int, training_place: str) -> list[ExerciseModel]:
        query = select(ExerciseModel).where(
            ExerciseModel.muscle_group_id == muscle_group_id,
            ExerciseModel.training_place == training_place
        )
        result = await self.db.execute(query)
        return result.scalars().all()


    async def create(self, name: str, sets_number: int, repetitions: int, training_place: str, gems: int, expirience_level: str, muscle_group_id: int) -> ExerciseModel:
        exercise = ExerciseModel(
            name=name,
            sets_number=sets_number,
            repetitions=repetitions,
            training_place=training_place,
            gems=gems,
            expirience_level=expirience_level,
            muscle_group_id=muscle_group_id
        )
        self.db.add(exercise)
        await self.db.commit()
        await self.db.refresh(exercise)
        return exercise


    async def get_all(self) -> list[ExerciseModel]:
        query = select(ExerciseModel)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_name(self, name: str) -> ExerciseModel | None:
        query = select(ExerciseModel).where(ExerciseModel.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
