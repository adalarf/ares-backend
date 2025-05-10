from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.auth.models.user import GenderEnum, GoalEnum, ActivityEnum, TrainingPlaceEnum, LoadEnum


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    gender: Optional[GenderEnum] = None
    age: Optional[int] = None
    goal: Optional[GoalEnum] = None
    activity: Optional[ActivityEnum] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    training_place: Optional[TrainingPlaceEnum] = None
    load: Optional[LoadEnum] = None
    restrictions: Optional[list[str]] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    gender: Optional[GenderEnum] = None
    goal: Optional[GoalEnum] = None
    activity: Optional[ActivityEnum] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    training_place: Optional[TrainingPlaceEnum] = None
    load: Optional[LoadEnum] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserInfo(BaseModel):
    id: int
    gems: int
    level: int
    experience_to_next_level: int
    experience_current: int


class CaloriesInfo(BaseModel):
    body_mass_index: float
