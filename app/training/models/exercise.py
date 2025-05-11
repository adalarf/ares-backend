from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base


class ExerciseModel(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    training_place = Column(String, nullable=False)
    image = Column(String, nullable=True)

    sets_number_default = Column(Integer, nullable=False)
    repetitions_default = Column(Integer, nullable=False)
    gems_default = Column(Integer, nullable=False)
    expirience_default = Column(Integer, nullable=False)
    expirience_level = Column(String, nullable=False)
    intensity = Column(String, nullable=True)

    kg50_calories = Column(Float, nullable=True)
    kg60_calories = Column(Float, nullable=True)
    kg70_calories = Column(Float, nullable=True)
    kg80_calories = Column(Float, nullable=True)
    kg90_calories = Column(Float, nullable=True)
    kg100_calories = Column(Float, nullable=True)



    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id", ondelete="CASCADE"), nullable=False)
    # exercise_type_id = Column(Integer, ForeignKey("exercise_types.id", ondelete="CASCADE"), nullable=False)
    
    planned_exercises = relationship("PlannedExerciseModel", back_populates="exercise")
    muscle_group = relationship("MuscleGroupModel", back_populates="exercises")
    random_exercises = relationship("RandomExerciseModel", back_populates="exercise")
    # exercise_type = relationship("ExerciseTypeModel", back_populates="exercises")
