import json
import uuid
from datetime import datetime, timedelta

import aiosqlite

DB_PATH = "nutrimind.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id TEXT PRIMARY KEY,
                food_name TEXT NOT NULL,
                image_url TEXT,
                nutrition_json TEXT NOT NULL,
                health_score INTEGER NOT NULL,
                ingredients_json TEXT NOT NULL,
                actions_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_meal(meal_data: dict) -> str:
    meal_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO meals (id, food_name, image_url, nutrition_json,
               health_score, ingredients_json, actions_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                meal_id,
                meal_data["food_name"],
                meal_data.get("image_url"),
                json.dumps(meal_data["nutrition"], ensure_ascii=False),
                meal_data["health_score"],
                json.dumps(meal_data["ingredients"], ensure_ascii=False),
                json.dumps(meal_data["actions"], ensure_ascii=False),
                now,
            ),
        )
        await db.commit()
    return meal_id


async def get_meals(limit: int = 50) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM meals ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
    return [_row_to_meal(row) for row in rows]


async def get_meal_by_id(meal_id: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
        row = await cursor.fetchone()
    return _row_to_meal(row) if row else None


async def get_today_meals() -> list[dict]:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM meals WHERE created_at >= ? ORDER BY created_at DESC",
            (today_start.isoformat(),),
        )
        rows = await cursor.fetchall()
    return [_row_to_meal(row) for row in rows]


async def get_dashboard_stats() -> dict:
    meals = await get_meals(limit=200)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=6)

    today_meals = [m for m in meals if datetime.fromisoformat(m["created_at"]) >= today_start]

    weekly: dict[str, float] = {}
    for i in range(7):
        day = (week_start + timedelta(days=i)).strftime("%m/%d")
        weekly[day] = 0.0

    for meal in meals:
        dt = datetime.fromisoformat(meal["created_at"])
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


def _row_to_meal(row: aiosqlite.Row) -> dict:
    return {
        "id": row["id"],
        "food_name": row["food_name"],
        "image_url": row["image_url"],
        "nutrition": json.loads(row["nutrition_json"]),
        "health_score": row["health_score"],
        "ingredients": json.loads(row["ingredients_json"]),
        "actions": json.loads(row["actions_json"]),
        "created_at": row["created_at"],
    }
