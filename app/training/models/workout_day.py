from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class WorkoutDayModel(Base):
    __tablename__ = "workout_days"

    id = Column(Integer, primary_key=True, index=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plan.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)

    workout_plan = relationship("WorkoutPlanModel", back_populates="workout_days")
    planned_exercises = relationship("PlannedExerciseModel", back_populates="workout_day")
    muscle_group = relationship("MuscleGroupModel", back_populates="workout_days")
