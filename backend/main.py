from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db
from app.routers import dashboard, meals, reports, scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception:
        # Keep API alive (scan/coach) even if DB init fails on cold start.
        import logging

        logging.exception("Database initialization failed")
    yield


app = FastAPI(
    title="NutriMind AI",
    description="Snap. Analyze. Improve. — AI Nutrition Coach API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router)
app.include_router(meals.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/api/health")
async def health():
    db_status = "sqlite"
    if settings.is_production_db:
        db_status = "postgresql"
        try:
            from app.db.pg import connect_postgres

            conn = await connect_postgres(settings.normalized_database_url)
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
            await conn.close()
            db_status = "postgresql:connected"
        except Exception as exc:
            db_status = f"postgresql:error:{type(exc).__name__}:{str(exc)[:160]}"

    return {
        "status": "ok",
        "service": "NutriMind AI",
        "openai_configured": bool(settings.openai_api_key),
        "database": db_status,
        "vercel": settings.is_vercel,
    }
