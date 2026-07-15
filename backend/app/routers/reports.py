from fastapi import APIRouter, HTTPException

from app.models.schemas import WeeklyReport
from app.services import report_service

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/weekly", response_model=WeeklyReport)
async def get_weekly_report():
    try:
        report = await report_service.create_weekly_report()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {e}")

    return WeeklyReport(**report)
