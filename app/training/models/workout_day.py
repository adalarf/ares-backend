from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database import Base
from sqlalchemy.orm import relationship


class WorkoutDayModel(Base):
    __tablename__ = "workout_days"

    id = Column(Integer, primary_key=True, index=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plan.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    workout_plan = relationship("WorkoutPlanModel", back_populates="workout_days")
