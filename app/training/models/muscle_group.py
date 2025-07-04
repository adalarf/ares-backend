from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.training.models.user_injury import user_injury


class MuscleGroupModel(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)

    exercises = relationship("ExerciseModel", back_populates="muscle_group")
    workout_days = relationship("WorkoutDayModel", back_populates="muscle_group")

    injured_users = relationship("UserModel", secondary=user_injury, back_populates="injuries")
