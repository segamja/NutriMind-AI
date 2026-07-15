from fastapi import APIRouter, HTTPException

from app.db import database as db
from app.models.schemas import CoachRequest, CoachResponse, MealCreate, MealRecord
from app.services.openai_service import get_coaching_response

router = APIRouter(tags=["meals", "coach"])


@router.post("/api/meals", response_model=MealRecord)
async def create_meal(meal: MealCreate):
    meal_id = await db.save_meal(meal.model_dump())
    saved = await db.get_meal_by_id(meal_id)
    if not saved:
        raise HTTPException(status_code=500, detail="Failed to save meal")
    return MealRecord(**saved)


@router.get("/api/meals", response_model=list[MealRecord])
async def list_meals(limit: int = 50):
    meals = await db.get_meals(limit=limit)
    return [MealRecord(**m) for m in meals]


@router.get("/api/meals/today", response_model=list[MealRecord])
async def list_today_meals():
    meals = await db.get_today_meals()
    return [MealRecord(**m) for m in meals]


@router.post("/api/coach", response_model=CoachResponse)
async def chat_with_coach(request: CoachRequest):
    today_meals = request.today_meals
    if not today_meals:
        today_meals_data = await db.get_today_meals()
        today_meals = [MealRecord(**m) for m in today_meals_data]

    history = [{"role": m.role, "content": m.content} for m in request.history]
    meals_data = [m.model_dump() for m in today_meals]

    try:
        result = get_coaching_response(request.message, history, meals_data)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coach request failed: {e}")

    return CoachResponse(**result)
