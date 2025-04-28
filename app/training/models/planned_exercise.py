from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class PlannedExerciseModel(Base):
    __tablename__ = "planned_exercises"

    id = Column(Integer, primary_key=True, index=True)
    sets_number = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    gems = Column(Integer, nullable=False)
    expirience = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    workout_day_id = Column(Integer, ForeignKey("workout_days.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)

    workout_day = relationship("WorkoutDayModel", back_populates="planned_exercises")
    exercise = relationship("ExerciseModel", back_populates="planned_exercises")
