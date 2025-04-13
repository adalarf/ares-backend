from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class PlannedExerciseModel(Base):
    __tablename__ = "planned_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_day_id = Column(Integer, ForeignKey("workout_days.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)

    workout_day = relationship("WorkoutDayModel", back_populates="planned_exercises")
    exercise = relationship("ExerciseModel", back_populates="planned_exercises")
