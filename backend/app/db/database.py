import json
import uuid
from datetime import datetime, timedelta
from typing import Any

from app.config import settings

USE_POSTGRES = settings.is_production_db and not settings.use_supabase_rest
USE_SUPABASE_REST = settings.use_supabase_rest


async def init_db() -> None:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        await rest.init_db()
    elif USE_POSTGRES:
        await _init_postgres()
    else:
        await _init_sqlite()


async def save_meal(meal_data: dict) -> str:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.save_meal(meal_data)
    if USE_POSTGRES:
        return await _save_meal_postgres(meal_data)
    return await _save_meal_sqlite(meal_data)


async def get_meals(limit: int = 50) -> list[dict]:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.get_meals(limit)
    if USE_POSTGRES:
        return await _get_meals_postgres(limit)
    return await _get_meals_sqlite(limit)


async def get_meal_by_id(meal_id: str) -> dict | None:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.get_meal_by_id(meal_id)
    if USE_POSTGRES:
        return await _get_meal_by_id_postgres(meal_id)
    return await _get_meal_by_id_sqlite(meal_id)


async def get_today_meals() -> list[dict]:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.get_today_meals()
    if USE_POSTGRES:
        return await _get_today_meals_postgres()
    return await _get_today_meals_sqlite()


async def get_meals_since(days: int = 7) -> list[dict]:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.get_meals_since(days)
    if USE_POSTGRES:
        return await _get_meals_since_postgres(days)
    return await _get_meals_since_sqlite(days)


async def get_dashboard_stats() -> dict:
    if USE_SUPABASE_REST:
        from app.db import supabase_rest as rest

        return await rest.get_dashboard_stats()
    return await _get_dashboard_stats_local()


async def _get_dashboard_stats_local() -> dict:
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


def _row_to_meal(row: Any) -> dict:
    if USE_POSTGRES:
        return {
            "id": row["id"],
            "food_name": row["food_name"],
            "image_url": row["image_url"],
            "nutrition": row["nutrition_json"] if isinstance(row["nutrition_json"], dict) else json.loads(row["nutrition_json"]),
            "health_score": row["health_score"],
            "ingredients": row["ingredients_json"] if isinstance(row["ingredients_json"], list) else json.loads(row["ingredients_json"]),
            "actions": row["actions_json"] if isinstance(row["actions_json"], list) else json.loads(row["actions_json"]),
            "created_at": row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"]),
        }

    import aiosqlite
    assert isinstance(row, aiosqlite.Row)
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


# --- PostgreSQL (Supabase) ---

async def _pg_connect():
    from app.db.pg import connect_postgres

    return await connect_postgres(settings.normalized_database_url)


async def _init_postgres() -> None:
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS meals (
                    id TEXT PRIMARY KEY,
                    food_name TEXT NOT NULL,
                    image_url TEXT,
                    nutrition_json JSONB NOT NULL,
                    health_score INTEGER NOT NULL,
                    ingredients_json JSONB NOT NULL,
                    actions_json JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
    finally:
        await conn.close()


async def _save_meal_postgres(meal_data: dict) -> str:
    meal_id = str(uuid.uuid4())
    now = datetime.utcnow()
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO meals (id, food_name, image_url, nutrition_json,
                   health_score, ingredients_json, actions_json, created_at)
                   VALUES (%s, %s, %s, %s::jsonb, %s, %s::jsonb, %s::jsonb, %s)""",
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
    finally:
        await conn.close()
    return meal_id


async def _get_meals_postgres(limit: int) -> list[dict]:
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM meals ORDER BY created_at DESC LIMIT %s",
                (limit,),
            )
            rows = await cur.fetchall()
    finally:
        await conn.close()
    return [_row_to_meal(dict(row)) for row in rows]


async def _get_meal_by_id_postgres(meal_id: str) -> dict | None:
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM meals WHERE id = %s", (meal_id,))
            row = await cur.fetchone()
    finally:
        await conn.close()
    return _row_to_meal(dict(row)) if row else None


async def _get_today_meals_postgres() -> list[dict]:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM meals WHERE created_at >= %s ORDER BY created_at DESC",
                (today_start,),
            )
            rows = await cur.fetchall()
    finally:
        await conn.close()
    return [_row_to_meal(dict(row)) for row in rows]


async def _get_meals_since_postgres(days: int) -> list[dict]:
    since = datetime.utcnow() - timedelta(days=days)
    conn = await _pg_connect()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM meals WHERE created_at >= %s ORDER BY created_at ASC",
                (since,),
            )
            rows = await cur.fetchall()
    finally:
        await conn.close()
    return [_row_to_meal(dict(row)) for row in rows]


# --- SQLite (local dev / Vercel fallback) ---

DB_PATH = "/tmp/nutrimind.db" if settings.is_vercel else "nutrimind.db"


async def _init_sqlite() -> None:
    import aiosqlite
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


async def _save_meal_sqlite(meal_data: dict) -> str:
    import aiosqlite
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


async def _get_meals_sqlite(limit: int) -> list[dict]:
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM meals ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
    return [_row_to_meal(row) for row in rows]


async def _get_meal_by_id_sqlite(meal_id: str) -> dict | None:
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
        row = await cursor.fetchone()
    return _row_to_meal(row) if row else None


async def _get_today_meals_sqlite() -> list[dict]:
    import aiosqlite
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM meals WHERE created_at >= ? ORDER BY created_at DESC",
            (today_start.isoformat(),),
        )
        rows = await cursor.fetchall()
    return [_row_to_meal(row) for row in rows]


async def _get_meals_since_sqlite(days: int) -> list[dict]:
    import aiosqlite
    since = datetime.utcnow() - timedelta(days=days)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM meals WHERE created_at >= ? ORDER BY created_at ASC",
            (since.isoformat(),),
        )
        rows = await cursor.fetchall()
    return [_row_to_meal(row) for row in rows]
