from app.training.repositories.workout_plan_repository import WorkoutPlanRepository
from app.training.repositories.workout_day_repository import WorkoutDayRepository
from app.training.repositories.planned_exercise_repository import PlannedExerciseRepository
from app.training.entities.workout_plan import WorkoutPlanCreation
from app.training.repositories.muscle_group_repository import MuscleGroupRepository
from app.training.repositories.muscle_group_repository import ExerciseRepository
from app.training.repositories.random_exercise_repository import RandomExerciseRepository
from app.training.entities.planned_exercise import PlannedExerciseCreation
from app.training.entities.workout_plan import WeeklyWorkoutPlanResponse, WorkoutDayInfo, ExerciseInfo
import random
from app.training.entities.workout_plan import WorkoutPlanResponse
from app.training.entities.exercise import ExerciseCreation, ExerciseResponse
from app.training.entities.random_exercise import RandomExerciseCreation, RandomExerciseInfo
from app.training.models.workout_plan import WorkoutPlanModel
from app.training.models.workout_day import WorkoutDayModel
from datetime import date, timedelta


class TrainingService:
    def __init__(self, workout_plan_repo: WorkoutPlanRepository, 
                 workout_day_repo: WorkoutDayRepository, 
                 planned_exercise_repo: PlannedExerciseRepository,
                 exercise_repo: ExerciseRepository,
                 random_exercise_repo: RandomExerciseRepository,
                 muscle_group_repo: MuscleGroupRepository):
        self.workout_plan_repo = workout_plan_repo
        self.workout_day_repo = workout_day_repo
        self.planned_exercise_repo = planned_exercise_repo
        self.exercise_repo = exercise_repo
        self.muscle_group_repo = muscle_group_repo
        self.random_exercise_repo = random_exercise_repo


    async def create_weekly_workout_plan(self, workout_plan_data: WorkoutPlanCreation, user_id: int) -> WeeklyWorkoutPlanResponse:
        existing_plan = await self.workout_plan_repo.get_by_user_id(user_id)
        if existing_plan:
            return await self.get_workout_plan_by_id(existing_plan[0].id)
        days_per_week = self.determine_days_per_week(workout_plan_data.training_level)
        workout_plan = await self.create_workout_plan(user_id, workout_plan_data)
        await self.assign_workout_days(workout_plan, days_per_week, workout_plan_data)
        workout_days = await self.workout_day_repo.get_by_workout_plan_id(workout_plan.id)

        result_days = []
        for workout_day in workout_days:
            planned_exercises = await self.planned_exercise_repo.get_by_workout_day_id(workout_day.id)
            exercises_info = [
                ExerciseInfo(
                    exercise_id=exercise.exercise_id,
                    workout_day_id=exercise.workout_day_id,
                    sets_number=exercise.sets_number,
                    repetitions=exercise.repetitions,
                    gems=exercise.gems,
                    expirience=exercise.expirience,
                    name=exercise.exercise.name,
                    image=exercise.exercise.image or ""
                )
                for exercise in planned_exercises
            ]
            result_days.append(WorkoutDayInfo(
                id=workout_day.id,
                day_of_week=workout_day.day_of_week,
                date=workout_day.date.strftime("%Y-%m-%d") if workout_day.date else None,
                image=workout_day.muscle_group.image or "",
                muscle_group=workout_day.muscle_group.name,
                exercises=exercises_info
            ))

        return WeeklyWorkoutPlanResponse(
            workout_plan_id=workout_plan.id,
            user_id=workout_plan.user_id,
            days=result_days,
            week_start_date=workout_plan.week_start_date.strftime("%Y-%m-%d"),
            week_end_date=workout_plan.week_end_date.strftime("%Y-%m-%d")
        )


    def determine_days_per_week(self, training_level: str):
        return {
            'low': 3,
            'middle': 4,
            'high': 5
        }.get(training_level, 3)


    async def create_workout_plan(self, user_id: int, workout_plan_data: WorkoutPlanCreation) -> WorkoutPlanModel:
        workout_plan = WorkoutPlanModel(
            user_id=user_id,
            week_start_date=date.today(),
            week_end_date=date.today() + timedelta(days=6)
        )
        return await self.workout_plan_repo.create(workout_plan)


    async def assign_workout_days(self, workout_plan: WorkoutPlanModel, days_per_week: int, workout_plan_data: WorkoutPlanCreation):
        muscle_groups = await self.muscle_group_repo.get_all()
        random.shuffle(muscle_groups)
        selected_groups = muscle_groups[:days_per_week]

        workout_days = []
        for day_index, muscle_group in enumerate(selected_groups):
            workout_day = await self.create_workout_day(workout_plan, day_index, muscle_group.id)
            await self.assign_exercises_to_day(workout_day, muscle_group.name, workout_plan_data)
            workout_days.append(workout_day)

        return workout_days


    async def create_workout_day(self, workout_plan: WorkoutPlanModel, day_index: int, muscle_group_id: int = None, workout_day_date: date = None) -> WorkoutDayModel:
        workout_day = WorkoutDayModel(
            workout_plan_id=workout_plan.id,
            day_of_week=["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"][day_index],
            date=workout_day_date or date(2025, 4, 13),
            muscle_group_id=muscle_group_id
        )
        return await self.workout_day_repo.create(workout_day)


    async def assign_exercises_to_day(self, workout_day: WorkoutDayModel, muscle_group: str, 
                                      workout_plan_data: WorkoutPlanCreation):
        exercises = await self.get_exercises_for_muscle_group(muscle_group, workout_plan_data.training_place)

        if not exercises:
            print(f"No exercises found for muscle group: {muscle_group} and place: {workout_plan_data.training_place}")
            return

        for exercise in exercises[:3]:
            planned_exercise = PlannedExerciseCreation(
                workout_day_id=workout_day.id,
                exercise_id=exercise.id,
                sets_number=exercise.sets_number_default,
                repetitions=exercise.repetitions_default,
                gems=exercise.gems_default,
                expirience=exercise.expirience_default
            )
            await self.planned_exercise_repo.create(planned_exercise)


    async def get_exercises_for_muscle_group(self, muscle_group: str, training_place: str):
        muscle_group_model = await self.muscle_group_repo.get_by_name(muscle_group)
        if not muscle_group_model:
            print(f"Muscle group not found: {muscle_group}")
            return []

        exercises = await self.exercise_repo.get_by_muscle_group_and_place(
            muscle_group_id=muscle_group_model.id,
            training_place=training_place
        )

        if not exercises:
            print(f"No exercises found for muscle group ID: {muscle_group_model.id} and place: {training_place}")

        return exercises


    async def get_workout_plan_id_by_user_id(self, user_id: int) -> int:
        workout_plan = await self.workout_plan_repo.get_by_user_id(user_id)
        if not workout_plan:
            raise ValueError(f"Workout plan for user ID {user_id} not found.")
        return workout_plan[0].id


    async def get_workout_plan_by_id(self, workout_plan_id: int) -> WeeklyWorkoutPlanResponse:
        workout_plan = await self.workout_plan_repo.get_by_id(workout_plan_id)
        if not workout_plan:
            raise ValueError(f"Workout plan with ID {workout_plan_id} not found.")

        workout_days = await self.workout_day_repo.get_by_workout_plan_id(workout_plan_id)
        days_info = []
        for workout_day in workout_days:
            planned_exercises = await self.planned_exercise_repo.get_by_workout_day_id(workout_day.id)
            exercises_info = [
                ExerciseInfo(
                    exercise_id=exercise.exercise_id,
                    workout_day_id=exercise.workout_day_id,
                    sets_number=exercise.sets_number,
                    repetitions=exercise.repetitions,
                    gems=exercise.gems,
                    expirience=exercise.expirience,
                    name=exercise.exercise.name,
                    image=exercise.exercise.image or ""
                )
                for exercise in planned_exercises
            ]
            days_info.append(WorkoutDayInfo(
                id=workout_day.id,
                day_of_week=workout_day.day_of_week,
                date=workout_day.date.strftime("%Y-%m-%d") if workout_day.date else None,
                image=workout_day.muscle_group.image or "",
                muscle_group=workout_day.muscle_group.name,
                exercises=exercises_info
            ))

        return WeeklyWorkoutPlanResponse(
            workout_plan_id=workout_plan.id,
            user_id=workout_plan.user_id,
            week_start_date=workout_plan.week_start_date.strftime("%Y-%m-%d"),
            week_end_date=workout_plan.week_end_date.strftime("%Y-%m-%d"),
            days=days_info
        )


    async def create_muscle_groups(self, muscle_groups: list[dict]):
        for group in muscle_groups:
            existing_group = await self.muscle_group_repo.get_by_name(group["name"])
            if not existing_group:
                await self.muscle_group_repo.create(group["name"], group.get("image"))


    async def get_muscle_groups(self):
        muscle_groups = await self.muscle_group_repo.get_all()
        return [
            {
                "id": muscle_group.id,
                "name": muscle_group.name,
                "image": muscle_group.image
            }
            for muscle_group in muscle_groups
        ]


    async def create_exercises(self, exercises_data: list[ExerciseCreation]):
        created_exercises = []
        for exercise_data in exercises_data:
            existing_exercise = await self.exercise_repo.get_by_name(exercise_data.name)
            if not existing_exercise:
                created_exercise = await self.exercise_repo.create(
                    name=exercise_data.name,
                    training_place=exercise_data.training_place,
                    muscle_group_id=exercise_data.muscle_group_id,
                    sets_number_default=exercise_data.sets_number_default,
                    repetitions_default=exercise_data.repetitions_default,
                    gems_default=exercise_data.gems_default,
                    expirience_level=exercise_data.expirience_level,
                    expirience_default=exercise_data.expirience_default
                )
                created_exercises.append(created_exercise)
        return [
            ExerciseResponse(
                id=exercise.id,
                name=exercise.name,
                training_place=exercise.training_place,
                muscle_group_id=exercise.muscle_group_id
            )
            for exercise in created_exercises
        ]


    async def get_exercises(self, muscle_group_id: int = None) -> list[ExerciseResponse]:
        if (muscle_group_id is not None):
            exercises = await self.exercise_repo.get_by_muscle_group_id(muscle_group_id)
            # exercises = [e for e in exercises if e.muscle_group_id == muscle_group_id]
        else:
            exercises = await self.exercise_repo.get_all()
        return [
            ExerciseResponse(
                id=exercise.id,
                name=exercise.name,
                description=exercise.description,
                image=exercise.image or "",
                sets_number_default=exercise.sets_number_default,
                repetitions_default=exercise.repetitions_default,
                training_place=exercise.training_place,
                gems_default=exercise.gems_default,
                expirience_default=exercise.expirience_default,
                expirience_level=exercise.expirience_level,
                muscle_group_id=exercise.muscle_group_id
            )
            for exercise in exercises
        ]
    

    async def create_random_exercise(self, workout_plan_data: WorkoutPlanCreation, user_id: int):
        exercises = await self.exercise_repo.get_all()
        filtered = [e for e in exercises if e.training_place == workout_plan_data.training_place and e.expirience_level == workout_plan_data.training_level]
        if not filtered:
            return None
        exercise = random.choice(filtered)
        random_exercise = RandomExerciseCreation(
            exercise_id=exercise.id,
            user_id=user_id,
            sets_number=exercise.sets_number_default,
            repetitions=exercise.repetitions_default,
            gems=exercise.gems_default,
            expirience=exercise.expirience_default
        )
        random_exercise = await self.random_exercise_repo.create(random_exercise)

        return RandomExerciseInfo(
            id=random_exercise.id,
            exercise_id=random_exercise.exercise.id,
            sets_number=random_exercise.sets_number,
            repetitions=random_exercise.repetitions,
            gems=random_exercise.gems,
            expirience=random_exercise.expirience,
            name=random_exercise.exercise.name,
            image=random_exercise.exercise.image or ""
        )


    async def get_random_exercises_by_user(self, user_id: int):
        random_exercises = await self.random_exercise_repo.get_by_user_id(user_id)
        random_exercise = random_exercises[0] if random_exercises else None
        if not random_exercise:
            return None
        return RandomExerciseInfo(
            id=random_exercise.id,
            exercise_id=random_exercise.exercise.id,
            sets_number=random_exercise.sets_number,
            repetitions=random_exercise.repetitions,
            gems=random_exercise.gems,
            expirience=random_exercise.expirience,
            name=random_exercise.exercise.name,
            image=random_exercise.exercise.image or ""
        )
