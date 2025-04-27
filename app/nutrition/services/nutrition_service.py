from sqlalchemy import select
from fastapi import HTTPException
from app.nutrition.models.dish import DishModel
from app.nutrition.entities.dish import DishCreation
from app.nutrition.repositories.dish_repository import DishRepository
from app.nutrition.repositories.ingredient_repository import IngredientRepository
from app.nutrition.repositories.meal_plan_repository import MealPlanRepository
from app.nutrition.repositories.meal_repository import MealRepository
from typing import Dict, List
import random


class NutritionService:
    def __init__(self, dish_repo: DishRepository, 
                 ingredient_repo: IngredientRepository,
                 meal_plan_repo: MealPlanRepository,
                 meal_repo: MealRepository):
        self.dish_repo = dish_repo
        self.ingredient_repo = ingredient_repo
        self.meal_plan_repo = meal_plan_repo
        self.meal_repo = meal_repo


    def calculate_bmr(self, gender: str, goal: str, age: int, weight: float, height: float) -> float:
        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        if goal == "weight_loss":
            bmr *= 0.75
        elif goal == "muscle_gain":
            bmr *= 1.15

        return bmr
    

    def calculate_macros(calories: float, goal: str):
        if goal == "weight_loss":
            proteins = 0.3 * calories / 4  
            fats = 0.3 * calories / 9      
            carbs = 0.4 * calories / 4     
        else:
            proteins = 0.25 * calories / 4
            fats = 0.25 * calories / 9
            carbs = 0.5 * calories / 4
        
        return proteins, fats, carbs
    

    async def get_filtered_dishes(self, goal: str, restrictions: list[str]):
        return await self.dish_repo.filter_dishes(goal, restrictions)
    

    def get_meal_distribution(self, meals_per_day: int) -> Dict[str, float]:
        distributions = {
            3: {
                "Завтрак": 0.3,
                "Обед": 0.4,
                "Ужин": 0.3
            },
            4: {
                "Завтрак": 0.25,
                "Обед": 0.35,
                "Перекус": 0.15,
                "Ужин": 0.25
            }
        }
        
        return distributions.get(meals_per_day, {})
    

    def select_dish(self, filtered_dishes: List[DishModel], meal_type: str) -> DishModel:
        suitable_dishes = [
            dish for dish in filtered_dishes 
            if dish.category == meal_type
        ]

        if not suitable_dishes:
            raise HTTPException(
                status_code=404,
                detail=f"Нет блюд для приёма пищи: {meal_type} ({meal_type})"
            )

        return random.choice(suitable_dishes)
    

    def calculate_grams(self, dish: DishModel, meal_percentage: float, calories: float) -> float:
        meal_calories = meal_percentage * calories
        calories_coefficient = meal_calories / dish.calories
        grams = calories_coefficient * 100
        proteins = dish.proteins * calories_coefficient
        fats = dish.fats * calories_coefficient
        carbs = dish.carbs * calories_coefficient

        return grams, proteins, fats, carbs


    async def get_or_create_ingredient(self, name: str):
        ingredient = await self.ingredient_repo.get_by_name(name)
        if not ingredient:
            ingredient = await self.ingredient_repo.create(name=name)
        
        return ingredient

    async def create_dish(self, dish_data: DishCreation) -> DishModel:
        ingredients = []
        for ingredient_name in dish_data.ingredients:
            ingredient = await self.get_or_create_ingredient(ingredient_name)
            ingredients.append(ingredient)
        
        result = await self.dish_repo.create_dish(
            name=dish_data.name,
            calories=dish_data.calories,
            proteins=dish_data.proteins,
            fats=dish_data.fats,
            carbs=dish_data.carbs,
            category=dish_data.category,
            goal=dish_data.goal,
            ingredients=ingredients
        )
        
        return result


    async def create_meal_plan(self, user_id: int, plan_data: list[dict]):
        plan = await self.meal_plan_repo.create(user_id=user_id)
        meals = []
        for meal in plan_data:
            dish = await self.dish_repo.get_by_name(meal["dish"])
            meal_obj = await self.meal_repo.create(
                plan_id=plan.id,
                dish_id=dish.id,
                grams=meal["grams"],
                proteins=meal["proteins"],
                fats=meal["fats"],
                carbs=meal["carbs"]
            )
            meals.append(meal_obj)
        return plan, meals
