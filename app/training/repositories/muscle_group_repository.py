from sqlalchemy import select
from app.training.models.muscle_group import MuscleGroupModel
from app.training.models.exercise import ExerciseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class MuscleGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_name(self, name: str) -> MuscleGroupModel | None:
        query = select(MuscleGroupModel).where(MuscleGroupModel.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def create(self, name: str, image: str = None) -> MuscleGroupModel:
        muscle_group = MuscleGroupModel(name=name, image=image)
        self.db.add(muscle_group)
        await self.db.commit()
        await self.db.refresh(muscle_group)
        return muscle_group


    async def get_all(self) -> list[MuscleGroupModel]:
        query = select(MuscleGroupModel)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_id(self, id: int) -> MuscleGroupModel | None:
        query = select(MuscleGroupModel).where(MuscleGroupModel.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class ExerciseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get_by_muscle_group_id(self, id: int) -> list[ExerciseModel] | None:
        query = select(ExerciseModel).where(ExerciseModel.muscle_group_id == id)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_muscle_group_and_place(self, muscle_group_id: int, training_place: str) -> list[ExerciseModel]:
        query = select(ExerciseModel).options(selectinload(ExerciseModel.muscle_group)).where(
            ExerciseModel.muscle_group_id == muscle_group_id,
            ExerciseModel.training_place == training_place
        )
        result = await self.db.execute(query)
        return result.scalars().all()


    async def create(self, name: str, sets_number_default: int, 
                     repetitions_default: int, training_place: str, 
                     gems_default: int, expirience_level: str, 
                     muscle_group_id: int, expirience_default: int,
                     intensity: str, kg50_calories: float, kg60_calories: float, kg70_calories: float,
                     kg80_calories: float, kg90_calories: float, kg100_calories: float) -> ExerciseModel:
        exercise = ExerciseModel(
            name=name,
            training_place=training_place,
            sets_number_default=sets_number_default,
            repetitions_default=repetitions_default,
            gems_default=gems_default,
            expirience_default=expirience_default,
            expirience_level=expirience_level,
            muscle_group_id=muscle_group_id,
            intensity=intensity,
            kg50_calories=kg50_calories,
            kg60_calories=kg60_calories,
            kg70_calories=kg70_calories,
            kg80_calories=kg80_calories,
            kg90_calories=kg90_calories,
            kg100_calories=kg100_calories
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
