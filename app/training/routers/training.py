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
from app.training.repositories.random_exercise_repository import RandomExerciseRepository
from app.auth.repositories.user_repository import UserRepository
from app.training.entities.exercise import ExerciseCreation, ExerciseResponse
from app.training.entities.random_exercise import RandomExerciseInfo
from app.training.entities.muscle_group import MuscleGroupResponse, InjuriesUser


router = APIRouter()

def get_training_service(db: AsyncSession = Depends(get_async_session)) -> TrainingService:
    workout_plan_repo = WorkoutPlanRepository(db)
    workout_day_repo = WorkoutDayRepository(db)
    planned_exercise_repo = PlannedExerciseRepository(db)
    exercise_repo = ExerciseRepository(db)
    random_exercise_repo = RandomExerciseRepository(db)
    muscle_group_repo = MuscleGroupRepository(db)
    user_repo = UserRepository(db)
    return TrainingService(workout_plan_repo, workout_day_repo, 
                           planned_exercise_repo, exercise_repo, 
                           random_exercise_repo, muscle_group_repo,
                           user_repo)


@router.post("/workout_plan", response_model=WeeklyWorkoutPlanResponse)
async def create_workout_plan(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    return await training_service.create_weekly_workout_plan(current_user.id, 
                                                             current_user.activity.value,
                                                             current_user.training_place.value,
                                                             current_user.weight) 


@router.get("/workout_plan", response_model=WeeklyWorkoutPlanResponse | str)
async def get_workout_plan(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    workout_plan_id = await training_service.get_workout_plan_id_by_user_id(current_user.id)
    if not workout_plan_id:
        return f"Workout plan for user ID {current_user.id} not found."
    workout_plan = await training_service.get_workout_plan_by_id(workout_plan_id)
    if not workout_plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return workout_plan


@router.post("/random_exercise", response_model=RandomExerciseInfo)
async def create_random_exercise(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):  
    exercise = await training_service.create_random_exercise(current_user.training_place.value,
                                                             current_user.intensity, current_user.id)
    return exercise


@router.get("/random_exercise", response_model=RandomExerciseInfo)
async def get_random_exercise(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    random_exercise = await training_service.get_random_exercises_by_user(current_user.id)
    if random_exercise is None:
        raise HTTPException(status_code=404, detail="Случайное упражнение не найдено для данного пользователя")
    return random_exercise


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


@router.post("/injuries")
async def add_injury(muscle_group_names: InjuriesUser, 
                     current_user: User = Depends(get_current_user),
                     training_service: TrainingService = Depends(get_training_service)):
    result = await training_service.add_injury_to_user(current_user.id, muscle_group_names.injuries)

    return result


@router.post("/complete_exercise/{exercise_id}")
async def complete_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    await training_service.complete_planned_exercise(exercise_id, current_user)
    return {"message": "Exercise completed successfully"}


@router.post("/complete_random_exercise/{exercise_id}")
async def complete_random_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    await training_service.complete_random_exercise(exercise_id, current_user)
    return {"message": "Exercise completed successfully"}


@router.delete("/workout_plan")
async def delete_workout_plan(
    current_user: User = Depends(get_current_user),
    training_service: TrainingService = Depends(get_training_service)
):
    try:
        workout_plan_id = await training_service.get_workout_plan_id_by_user_id(current_user.id)
        
        await training_service.delete_workout_plan(workout_plan_id)
        
        return {"message": "План тренировок успешно удален"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении плана тренировок: {str(e)}")
