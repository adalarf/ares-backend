from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.services.auth_service import get_current_user
from app.training.services.training_service import TrainingService
from app.auth.entities.user import User
from app.training.entities.workout_plan import WorkoutPlanCreation, WeeklyWorkoutPlanResponse
from app.training.repositories.workout_plan_repository import WorkoutPlanRepository
from app.training.repositories.workout_day_repository import WorkoutDayRepository
from app.training.repositories.planned_exercise_repository import PlannedExerciseRepository
from app.training.repositories.muscle_group_repository import MuscleGroupRepository
from app.training.repositories.muscle_group_repository import ExerciseRepository
from app.training.entities.exercise import ExerciseCreation, ExerciseResponse
from app.training.entities.muscle_group import MuscleGroupResponse


router = APIRouter()

def get_training_service(db: AsyncSession = Depends(get_async_session)) -> TrainingService:
    workout_plan_repo = WorkoutPlanRepository(db)
    workout_day_repo = WorkoutDayRepository(db)
    planned_exercise_repo = PlannedExerciseRepository(db)
    exercise_repo = ExerciseRepository(db)
    muscle_group_repo = MuscleGroupRepository(db)
    return TrainingService(workout_plan_repo, workout_day_repo, 
                           planned_exercise_repo, exercise_repo, muscle_group_repo)


@router.post("/workout_plan", response_model=WeeklyWorkoutPlanResponse)
async def create_workout_plan(
    workout_plan_data: WorkoutPlanCreation,
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    return await training_service.create_weekly_workout_plan(workout_plan_data, current_user.id)


@router.get("/workout_plan", response_model=WeeklyWorkoutPlanResponse)
async def get_workout_plan(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    workout_plan_id = await training_service.get_workout_plan_id_by_user_id(current_user.id)
    workout_plan = await training_service.get_workout_plan_by_id(workout_plan_id)
    if not workout_plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return workout_plan


@router.post("/muscle_groups")
async def create_muscle_groups(
    muscle_groups: list[str],
    training_service: TrainingService = Depends(get_training_service)
):
    muscle_groups = await training_service.create_muscle_groups(muscle_groups)
    return muscle_groups


@router.get("/muscle_groups", response_model=list[MuscleGroupResponse])
async def get_muscle_groups(
    training_service: TrainingService = Depends(get_training_service)
):
    muscle_groups = await training_service.get_muscle_groups()
    return muscle_groups


@router.post("/exercises", response_model=list[ExerciseResponse])
async def create_exercises(
    exercises_data: list[ExerciseCreation],
    training_service: TrainingService = Depends(get_training_service)
):
    return await training_service.create_exercises(exercises_data)


@router.get("/exercises", response_model=list[ExerciseResponse])
async def get_exercises(
    muscle_group_id: int = None,
    training_service: TrainingService = Depends(get_training_service)
):
    exercises = await training_service.get_exercises(muscle_group_id)
    return exercises
