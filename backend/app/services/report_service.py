from datetime import datetime, timedelta

from app.db import database as db
from app.services.openai_service import generate_weekly_report


async def create_weekly_report() -> dict:
    meals = await db.get_meals_since(days=7)
    if not meals:
        raise ValueError("주간 리포트를 생성하려면 최소 1개 이상의 식사 기록이 필요합니다.")

    end_date = datetime.utcnow().date()
    start_date = (datetime.utcnow() - timedelta(days=6)).date()
    period = f"{start_date.isoformat()} ~ {end_date.isoformat()}"

    report = generate_weekly_report(meals, period)
    return report
