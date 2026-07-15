from fastapi import APIRouter

from app.db import database as db
from app.models.schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_stats():
    stats = await db.get_dashboard_stats()
    return DashboardStats(**stats)
