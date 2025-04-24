from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.services.auth_service import get_current_user
from app.nutrition.services.nutrition_service import NutritionService
from app.nutrition.entities.meal_plan import MealPlanCreation
from app.auth.entities.user import User


router = APIRouter()

def get_nutrition_service(db: AsyncSession = Depends(get_async_session)) -> NutritionService:
    return NutritionService(db)

