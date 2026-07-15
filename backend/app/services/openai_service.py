import base64
import json
from typing import Any

from openai import OpenAI

from app.config import settings
from app.models.schemas import CNNResult, VisionAnalysis

VISION_SCHEMA = {
    "type": "object",
    "properties": {
        "food_name": {"type": "string"},
        "description": {"type": "string"},
        "ingredients": {"type": "array", "items": {"type": "string"}},
        "cooking_method": {"type": "string"},
        "portions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount_g": {"type": "number"},
                    "confidence": {"type": "number"},
                },
                "required": ["name", "amount_g", "confidence"],
                "additionalProperties": False,
            },
        },
        "nutrition": {
            "type": "object",
            "properties": {
                "calories": {"type": "number"},
                "protein": {"type": "number"},
                "fat": {"type": "number"},
                "carbohydrates": {"type": "number"},
                "fiber": {"type": "number"},
                "sugar": {"type": "number"},
                "sodium": {"type": "number"},
                "calcium": {"type": "number"},
                "iron": {"type": "number"},
                "potassium": {"type": "number"},
            },
            "required": [
                "calories", "protein", "fat", "carbohydrates",
                "fiber", "sugar", "sodium", "calcium", "iron", "potassium",
            ],
            "additionalProperties": False,
        },
        "health_score": {
            "type": "object",
            "properties": {
                "overall": {"type": "integer"},
                "calories": {"type": "integer"},
                "protein": {"type": "integer"},
                "fat": {"type": "integer"},
                "carbohydrates": {"type": "integer"},
                "sugar": {"type": "integer"},
                "sodium": {"type": "integer"},
                "fiber": {"type": "integer"},
            },
            "required": [
                "overall", "calories", "protein", "fat",
                "carbohydrates", "sugar", "sodium", "fiber",
            ],
            "additionalProperties": False,
        },
        "actions": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "food_name", "description", "ingredients", "cooking_method",
        "portions", "nutrition", "health_score", "actions",
    ],
    "additionalProperties": False,
}

COACH_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {"type": "string"},
        "actions": {"type": "array", "items": {"type": "string"}},
        "suggestions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["reply", "actions", "suggestions"],
    "additionalProperties": False,
}

WEEKLY_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "period": {"type": "string"},
        "total_meals": {"type": "integer"},
        "habit_analysis": {"type": "string"},
        "nutrient_analysis": {"type": "string"},
        "avg_health_score": {"type": "number"},
        "improvements": {"type": "array", "items": {"type": "string"}},
        "next_week_goals": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": [
        "period", "total_meals", "habit_analysis", "nutrient_analysis",
        "avg_health_score", "improvements", "next_week_goals", "summary",
    ],
    "additionalProperties": False,
}


def _get_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=settings.openai_api_key)


def _text_format(schema: dict, name: str) -> dict:
    return {
        "format": {
            "type": "json_schema",
            "name": name,
            "strict": True,
            "schema": schema,
        }
    }


def _responses_json(
    client: OpenAI,
    *,
    model: str,
    input_data: Any,
    instructions: str | None,
    schema: dict,
    name: str,
) -> dict:
    kwargs: dict = {
        "model": model,
        "input": input_data,
        "text": _text_format(schema, name),
    }
    if instructions:
        kwargs["instructions"] = instructions

    response = client.responses.create(**kwargs)
    return json.loads(response.output_text)


def analyze_food_image(
    image_bytes: bytes,
    cnn_hint: CNNResult,
    mime_type: str = "image/jpeg",
) -> VisionAnalysis:
    client = _get_client()
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    prompt = f"""You are NutriMind AI, an expert nutrition analyst.
Analyze this food photo and provide detailed nutrition analysis in Korean.

CNN preliminary classification: {cnn_hint.food_name} (confidence: {cnn_hint.confidence})

Provide:
1. Accurate food name and description
2. List of visible ingredients
3. Estimated cooking method
4. Portion sizes in grams for each component
5. Full nutrition breakdown (calories, protein, fat, carbs, fiber, sugar, sodium, calcium, iron, potassium)
6. Health score (0-100) for overall meal and each nutrient aspect
7. 2-4 actionable recommendations in Korean (what the user should do next)

Be realistic with portion estimates based on visual cues."""

    data = _responses_json(
        client,
        model=settings.openai_vision_model,
        input_data=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": f"data:{mime_type};base64,{b64}"},
            ],
        }],
        instructions=None,
        schema=VISION_SCHEMA,
        name="food_analysis",
    )
    return VisionAnalysis(**data)


def get_coaching_response(
    message: str,
    history: list[dict],
    today_meals: list[dict],
) -> dict:
    client = _get_client()

    meals_context = ""
    if today_meals:
        meals_context = "\n\n오늘 식사 기록:\n"
        for meal in today_meals:
            n = meal.get("nutrition", {})
            meals_context += (
                f"- {meal.get('food_name')}: {n.get('calories', 0):.0f}kcal, "
                f"단백질 {n.get('protein', 0):.1f}g, "
                f"건강점수 {meal.get('health_score', 0)}점\n"
            )

    instructions = f"""You are NutriMind AI, a friendly Korean nutrition coach.
Help users improve their eating habits with practical, actionable advice.
Always respond in Korean. Be encouraging but honest.
{meals_context}

Provide:
1. A helpful reply to the user's question
2. 1-3 specific actions they can take today
3. 1-2 meal or food suggestions if relevant"""

    input_messages: list[dict] = []
    for msg in history[-10:]:
        input_messages.append({"role": msg["role"], "content": msg["content"]})
    input_messages.append({"role": "user", "content": message})

    return _responses_json(
        client,
        model=settings.openai_model,
        input_data=input_messages,
        instructions=instructions,
        schema=COACH_SCHEMA,
        name="coach_response",
    )


def generate_weekly_report(meals: list[dict], period: str) -> dict:
    client = _get_client()

    meals_summary = ""
    for meal in meals:
        n = meal.get("nutrition", {})
        meals_summary += (
            f"- {meal.get('food_name')} ({meal.get('created_at', '')[:10]}): "
            f"{n.get('calories', 0):.0f}kcal, 단백질 {n.get('protein', 0):.1f}g, "
            f"지방 {n.get('fat', 0):.1f}g, 탄수 {n.get('carbohydrates', 0):.1f}g, "
            f"건강점수 {meal.get('health_score', 0)}점\n"
        )

    instructions = """You are NutriMind AI, an expert nutrition analyst.
Analyze the user's weekly meal records and generate a comprehensive health report in Korean.
Be specific, actionable, and encouraging."""

    prompt = f"""다음은 사용자의 최근 7일간 식사 기록입니다.

분석 기간: {period}
총 식사 수: {len(meals)}회

{meals_summary}

위 데이터를 바탕으로 주간 건강 리포트를 작성해주세요.
period 필드에는 "{period}"를 사용하세요.
total_meals 필드에는 {len(meals)}을 사용하세요."""

    return _responses_json(
        client,
        model=settings.openai_model,
        input_data=prompt,
        instructions=instructions,
        schema=WEEKLY_REPORT_SCHEMA,
        name="weekly_report",
    )
