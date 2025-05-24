from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from .database import async_session_maker
from app.auth.repositories.token_repository import TokenRepository
from .config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.training.repositories.workout_plan_repository import WorkoutPlanRepository
from app.training.services.training_service import TrainingService
from app.training.repositories.workout_day_repository import WorkoutDayRepository
from app.auth.repositories.user_repository import UserRepository
from app.training.repositories.planned_exercise_repository import PlannedExerciseRepository
from app.training.repositories.muscle_group_repository import MuscleGroupRepository, ExerciseRepository
from app.training.entities.workout_plan import WorkoutPlanCreation
from datetime import date, timedelta
from sqlalchemy import update
from app.training.models.workout_day import WorkoutDayModel


async def cleanup_expired_tokens():
    async with async_session_maker() as session:
        token_repository = TokenRepository(session)
        await token_repository.cleanup_expired_tokens()


async def cleanup_and_create_new_weekly_plans():
    async with async_session_maker() as session:
        workout_plan_repo = WorkoutPlanRepository(session)
        user_repo = UserRepository(session)
        workout_day_repo = WorkoutDayRepository(session)
        planned_exercise_repo = PlannedExerciseRepository(session)
        muscle_group_repo = MuscleGroupRepository(session)
        exercise_repo = ExerciseRepository(session)
        training_service = TrainingService(
            workout_plan_repo, workout_day_repo, planned_exercise_repo, exercise_repo, muscle_group_repo
        )
        all_plans = await workout_plan_repo.get_all()
        today = date.today()
        for plan in all_plans:
            if (today - plan.week_start_date).days >= 7:
                user_id = plan.user_id
                await workout_plan_repo.delete(plan.id)

                user = await user_repo.get_user(user_id)

                await training_service.create_weekly_workout_plan(user.id, user.activity.value, user.training_place.value)



async def complete_past_workout_days():
    today = date.today()
    async with async_session_maker() as session:
        query = (
            update(WorkoutDayModel)
            .where(WorkoutDayModel.date < today, WorkoutDayModel.is_completed == False)
            .values(is_completed=True)
        )
        await session.execute(query)
        await session.commit()


async def update_active_workout_day():
    today = date.today()
    async with async_session_maker() as session:
        await session.execute(
            update(WorkoutDayModel)
            .where(WorkoutDayModel.is_active == True)
            .values(is_active=False)
        )
        await session.execute(
            update(WorkoutDayModel)
            .where(WorkoutDayModel.date == today)
            .values(is_active=True)
        )
        await session.commit()


def setup_periodic_tasks(app: FastAPI):
    @app.on_event("startup")
    @repeat_every(seconds=60 * int(ACCESS_TOKEN_EXPIRE_MINUTES))
    async def cleanup_tokens_task():
        await cleanup_expired_tokens()
        await cleanup_and_create_new_weekly_plans()
        await complete_past_workout_days()
        await update_active_workout_day()
