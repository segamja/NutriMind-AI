from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db
from app.routers import dashboard, meals, reports, scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
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
    return {
        "status": "ok",
        "service": "NutriMind AI",
        "openai_configured": bool(settings.openai_api_key),
        "database": "postgresql" if settings.is_production_db else "sqlite",
    }
