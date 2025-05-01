from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class BlitzPollModel(Base):
    __tablename__ = "blitz_polls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    blitz_questions = relationship("BlitzQuestionModel", back_populates="blitz_poll", cascade="all, delete-orphan")
    user = relationship("UserModel", back_populates="blitz_polls")
