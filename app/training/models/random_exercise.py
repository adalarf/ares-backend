from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class RandomExerciseModel(Base):
    __tablename__ = "random_exercises"

    id = Column(Integer, primary_key=True, index=True)
    sets_number = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    gems = Column(Integer, nullable=False)
    expirience = Column(Integer, nullable=False)
    calories = Column(Float, nullable=False)

    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    exercise = relationship("ExerciseModel", back_populates="random_exercises")
    user = relationship("UserModel", back_populates="random_exercises")
