import json
import uuid
from datetime import datetime, timedelta
from typing import Any

import httpx

from app.config import settings


def _headers() -> dict[str, str]:
    key = settings.service_role_key
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _base_url() -> str:
    return settings.resolved_supabase_url.rstrip("/")


async def _request(method: str, path: str, **kwargs) -> Any:
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.request(method, f"{_base_url()}{path}", headers=_headers(), **kwargs)
        if res.status_code >= 400:
            raise RuntimeError(f"Supabase API error {res.status_code}: {res.text[:200]}")
        if res.status_code == 204 or not res.content:
            return None
        return res.json()


def _normalize_meal(row: dict) -> dict:
    nutrition = row.get("nutrition_json", {})
    ingredients = row.get("ingredients_json", [])
    actions = row.get("actions_json", [])
    created_at = row.get("created_at", "")

    return {
        "id": row["id"],
        "food_name": row["food_name"],
        "image_url": row.get("image_url"),
        "nutrition": nutrition if isinstance(nutrition, dict) else json.loads(nutrition),
        "health_score": row["health_score"],
        "ingredients": ingredients if isinstance(ingredients, list) else json.loads(ingredients),
        "actions": actions if isinstance(actions, list) else json.loads(actions),
        "created_at": created_at if isinstance(created_at, str) else str(created_at),
    }


async def init_db() -> None:
    return None


async def save_meal(meal_data: dict) -> str:
    meal_id = str(uuid.uuid4())
    rows = await _request(
        "POST",
        "/rest/v1/meals",
        json={
            "id": meal_id,
            "food_name": meal_data["food_name"],
            "image_url": meal_data.get("image_url"),
            "nutrition_json": meal_data["nutrition"],
            "health_score": meal_data["health_score"],
            "ingredients_json": meal_data["ingredients"],
            "actions_json": meal_data["actions"],
        },
    )
    if isinstance(rows, list) and rows:
        return rows[0]["id"]
    return meal_id


async def get_meals(limit: int = 50) -> list[dict]:
    rows = await _request(
        "GET",
        "/rest/v1/meals",
        params={
            "select": "*",
            "order": "created_at.desc",
            "limit": str(limit),
        },
    )
    return [_normalize_meal(row) for row in rows or []]


async def get_meal_by_id(meal_id: str) -> dict | None:
    rows = await _request(
        "GET",
        "/rest/v1/meals",
        params={"select": "*", "id": f"eq.{meal_id}", "limit": "1"},
    )
    if not rows:
        return None
    return _normalize_meal(rows[0])


async def get_today_meals() -> list[dict]:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    rows = await _request(
        "GET",
        "/rest/v1/meals",
        params={
            "select": "*",
            "created_at": f"gte.{today_start.isoformat()}Z",
            "order": "created_at.desc",
        },
    )
    return [_normalize_meal(row) for row in rows or []]


async def get_meals_since(days: int = 7) -> list[dict]:
    since = datetime.utcnow() - timedelta(days=days)
    rows = await _request(
        "GET",
        "/rest/v1/meals",
        params={
            "select": "*",
            "created_at": f"gte.{since.isoformat()}Z",
            "order": "created_at.asc",
        },
    )
    return [_normalize_meal(row) for row in rows or []]


async def get_dashboard_stats() -> dict:
    meals = await get_meals(limit=200)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=6)

    today_meals = [m for m in meals if datetime.fromisoformat(m["created_at"].replace("Z", "")) >= today_start]

    weekly: dict[str, float] = {}
    for i in range(7):
        day = (week_start + timedelta(days=i)).strftime("%m/%d")
        weekly[day] = 0.0

    for meal in meals:
        dt = datetime.fromisoformat(meal["created_at"].replace("Z", ""))
        if dt >= week_start:
            day_key = dt.strftime("%m/%d")
            weekly[day_key] = weekly.get(day_key, 0) + meal["nutrition"]["calories"]

    weekly_calories = [{"date": k, "calories": v} for k, v in weekly.items()]

    if not meals:
        return {
            "total_meals": 0,
            "avg_calories": 0,
            "avg_protein": 0,
            "avg_health_score": 0,
            "today_calories": 0,
            "today_protein": 0,
            "weekly_calories": weekly_calories,
        }

    return {
        "total_meals": len(meals),
        "avg_calories": sum(m["nutrition"]["calories"] for m in meals) / len(meals),
        "avg_protein": sum(m["nutrition"]["protein"] for m in meals) / len(meals),
        "avg_health_score": sum(m["health_score"] for m in meals) / len(meals),
        "today_calories": sum(m["nutrition"]["calories"] for m in today_meals),
        "today_protein": sum(m["nutrition"]["protein"] for m in today_meals),
        "weekly_calories": weekly_calories,
    }
