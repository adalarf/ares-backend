from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.services.auth_service import get_current_user
from app.nutrition.services.nutrition_service import NutritionService
from app.nutrition.entities.meal_plan import MealPlanCreation, MealCreate, MealPlanRead, MealRead
from app.nutrition.entities.dish import DishesCreation, DishesRestrictions
from app.nutrition.repositories.dish_repository import DishRepository
from app.nutrition.repositories.ingredient_repository import IngredientRepository
from app.nutrition.repositories.meal_plan_repository import MealPlanRepository
from app.nutrition.repositories.meal_repository import MealRepository
from app.auth.repositories.user_repository import UserRepository
from app.auth.entities.user import User


router = APIRouter()

def get_nutrition_service(db: AsyncSession = Depends(get_async_session)) -> NutritionService:
    dish_repo = DishRepository(db)
    ingredient_repo = IngredientRepository(db)
    meal_plan_repo = MealPlanRepository(db)
    meal_repo = MealRepository(db)
    user_repo = UserRepository(db)
    return NutritionService(dish_repo, ingredient_repo, meal_plan_repo, meal_repo, user_repo)


@router.post("/generate_meal_plan", response_model=MealPlanRead)
async def generate_meal_plan(
    nutrition_service: NutritionService = Depends(get_nutrition_service), 
    current_user: User = Depends(get_current_user)
):    
    calories = nutrition_service.calculate_bmr(
        current_user.gender.value, 
        current_user.goal.value, 
        current_user.age,
        current_user.weight,
        current_user.height
    )
    
    restriction_names = []
    if current_user.restrictions:
        for restriction in current_user.restrictions:
            if hasattr(restriction, 'name'):
                restriction_names.append(restriction.name)
            else:
                restriction_names.append(restriction)
    
    filtered_dishes = await nutrition_service.get_filtered_dishes(current_user.goal.value, restriction_names)
    meal_distribution = nutrition_service.get_meal_distribution(3)

    plan_data = []
    for meal_type, percentage in meal_distribution.items():
        dish = nutrition_service.select_dish(filtered_dishes, meal_type)
        grams, proteins, fats, carbs, meal_calories = nutrition_service.calculate_grams(dish, percentage, calories)
        plan_data.append({
            "meal": meal_type,
            "dish": dish.name,
            "grams": grams,
            "calories": meal_calories,
            "proteins": proteins,
            "fats": fats,
            "carbs": carbs
        })
    plan, meals = await nutrition_service.create_meal_plan(current_user.id, plan_data)
    
    user_calories = await nutrition_service.get_calories_info(current_user.id)
    
    return MealPlanRead(
        id=plan.id,
        user_id=plan.user_id,
        total_calories=plan.total_calories,
        proteins=plan.proteins,
        fats=plan.fats,
        carbs=plan.carbs,
        calories_burned=user_calories["calories_burned"],
        calories_eaten=user_calories["calories_eaten"],
        proteins_eaten=user_calories["proteins_eaten"],
        fats_eaten=user_calories["fats_eaten"],
        carbs_eaten=user_calories["carbs_eaten"],
        meals=[
            MealRead(
            id=meal.id,
            meal=meal_data["meal"],
            dish=meal.dish.name,
            image=meal.dish.image,
            grams=meal.grams,
            calories=meal.calories,
            proteins=meal.proteins,
            fats=meal.fats,
            carbs=meal.carbs,
            is_eaten=meal.is_eaten,
        )
        for meal, meal_data in zip(meals, plan_data)
        ]
    )


@router.get("/meal_plan", response_model=MealPlanRead)
async def get_meal_plan(
    nutrition_service: NutritionService = Depends(get_nutrition_service),
    current_user: User = Depends(get_current_user)
):
    meal_plan = await nutrition_service.get_meal_plan(current_user.id)
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    user_calories = await nutrition_service.get_calories_info(current_user.id)
    
    return MealPlanRead(
        id=meal_plan.id,
        user_id=meal_plan.user_id,
        total_calories=meal_plan.total_calories,
        proteins=meal_plan.proteins,
        fats=meal_plan.fats,
        carbs=meal_plan.carbs,
        calories_burned=user_calories["calories_burned"],
        calories_eaten=user_calories["calories_eaten"],
        proteins_eaten=user_calories["proteins_eaten"],
        fats_eaten=user_calories["fats_eaten"],
        carbs_eaten=user_calories["carbs_eaten"],
        meals=[
            MealRead(
                id=meal.id,
                meal=meal.dish.category,
                dish=meal.dish.name,
                image=meal.dish.image,
                grams=meal.grams,
                calories=meal.calories,
                proteins=meal.proteins,
                fats=meal.fats,
                carbs=meal.carbs,
                is_eaten=meal.is_eaten,
            ) for meal in meal_plan.meals
        ]
    )


@router.post("/dish")
async def create_dish(dishes_data: DishesCreation, nutrition_service: NutritionService = Depends(get_nutrition_service)):
    try:
        created_dishes = []
        for dish_data in dishes_data.dishes:
            dish = await nutrition_service.create_dish(dish_data)
            created_dishes.append(dish)
        return created_dishes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/make_meal_eaten/{id}", response_model=MealRead)
async def make_meal_eaten(id: int,
                          nutrition_service: NutritionService = Depends(get_nutrition_service)):
    meal = await nutrition_service.make_meal_eaten(id)

    return MealRead(
        id=meal.id,
        meal=meal.dish.category,
        dish=meal.dish.name,
        image=meal.dish.image,
        grams=meal.grams,
        calories=meal.calories,
        proteins=meal.proteins,
        fats=meal.fats,
        carbs=meal.carbs,
        is_eaten=meal.is_eaten
    )


@router.post("/restrictions")
async def add_restrictions(
    restrictions: list[str],
    nutrition_service: NutritionService = Depends(get_nutrition_service),
    current_user: User = Depends(get_current_user)
):
    updated_user = await nutrition_service.add_restrictions(current_user.id, restrictions)
    return updated_user


@router.post("/dish-restrictions")
async def add_dish_restrictions(
    dish_restrictions: DishesRestrictions, 
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    results = await nutrition_service.add_dish_restrictions(dish_restrictions)
    return results
