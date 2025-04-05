from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from .user import UserModel


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    access_token = Column(String, unique=True, nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    access_token_expires = Column(DateTime(timezone=True), nullable=False)
    refresh_token_expires = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="tokens") 