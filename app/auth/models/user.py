from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.nutrition.models.user_restriction import user_restriction
from app.auth.models.user_item import user_item
from app.training.models.user_injury import user_injury
import enum


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class GoalEnum(enum.Enum):
    weight_loss = "weight_loss"
    muscle_gain = "muscle_gain"
    increase_activity = "increase_activity"


class ActivityEnum(enum.Enum):
    low = "low"
    middle = "middle"
    high = "high"


class TrainingPlaceEnum(enum.Enum):
    home = "home"
    gym = "gym"
    mixed = "mixed"


class LoadEnum(enum.Enum):
    physical = "physical"
    intellegentive = "intellegentive"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    gender = Column(Enum(GenderEnum), nullable=True)
    age = Column(Integer, nullable=True)
    goal = Column(Enum(GoalEnum), nullable=True)
    activity = Column(Enum(ActivityEnum), nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    training_place = Column(Enum(TrainingPlaceEnum), nullable=True)
    load = Column(Enum(LoadEnum), nullable=True)
    workout_week_days = Column(Integer, default=3)
    intensity = Column(String, nullable=True, default="low")

    gems = Column(Integer, default=0)
    expirience = Column(Integer, default=0)
    avatar = Column(String, nullable=True)

    calories_burned_daily = Column(Float, default=0)
    calories_eaten_daily = Column(Float, default=0)
    proteins_eaten_daily = Column(Float, default=0)
    fats_eaten_daily = Column(Float, default=0)
    carbs_eaten_daily = Column(Float, default=0)

    tokens = relationship("TokenModel", back_populates="user", cascade="all, delete")
    workout_plans = relationship("WorkoutPlanModel", back_populates="user", cascade="all, delete")
    random_exercises = relationship("RandomExerciseModel", back_populates="user", cascade="all, delete")
    restrictions = relationship(
        "RestrictionModel", 
        secondary=user_restriction,
        back_populates="users"
    )
    blitz_polls = relationship("BlitzPollModel", back_populates="user", cascade="all, delete")
    items = relationship(
        "ItemModel",
        secondary=user_item,
        back_populates="users"
    )
    injuries = relationship("MuscleGroupModel", 
                            secondary=user_injury, 
                            back_populates="injured_users",
                            cascade="all")
    # restriction_details = relationship(
    #     "UserRestrictionModel",
    #     back_populates="user"
    # )


from app.nutrition.models.restriction import RestrictionModel