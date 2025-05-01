from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)

    answers = relationship("AnswerModel", back_populates="question", cascade="all, delete-orphan")
    blitz_questions = relationship("BlitzQuestionModel", back_populates="question")
