from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os
sys.path.append(os.path.join(sys.path[0], 'app'))
from app.nutrition.models.user_restriction import user_restriction
from app.nutrition.models.dish_ingredient import dish_ingredient
from app.nutrition.models.dish_restriction import dish_restriction
from app.auth.models.user_item import user_item
from app.nutrition.models.restriction import RestrictionModel
from app.auth.models.user import UserModel
from app.auth.models.token import TokenModel
from app.auth.models.item import ItemModel
from app.training.models.exercise_type import ExerciseTypeModel
from app.training.models.exercise import ExerciseModel
from app.training.models.workout_plan import WorkoutPlanModel
from app.training.models.workout_day import WorkoutDayModel
from app.training.models.planned_exercise import PlannedExerciseModel
from app.training.models.muscle_group import MuscleGroupModel
from app.training.models.random_exercise import RandomExerciseModel
from app.nutrition.models.dish import DishModel
from app.nutrition.models.ingridient import IngredientModel
from app.nutrition.models.meal import MealModel
from app.nutrition.models.meal_plan import MealPlanModel
from app.blitz_poll.models.blitz_poll import BlitzPollModel
from app.blitz_poll.models.blitz_question import BlitzQuestionModel
from app.blitz_poll.models.question import QuestionModel
from app.blitz_poll.models.answer import AnswerModel
from app.config import DATABASE_URL_ALEMBIC
from app.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
section = config.config_ini_section

# config.set_main_option("sqlalchemy.url", DATABASE_URL_ALEMBIC)
# config.set_section_option(section, "DATABASE_URL_ALEMBIC", DATABASE_URL_ALEMBIC)
config.set_main_option("sqlalchemy.url", DATABASE_URL_ALEMBIC)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
