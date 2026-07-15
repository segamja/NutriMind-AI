import base64
import json

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


def _get_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=settings.openai_api_key)


def analyze_food_image(image_bytes: bytes, cnn_hint: CNNResult) -> VisionAnalysis:
    client = _get_client()
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    mime = "image/jpeg"

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

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                ],
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "food_analysis",
                "strict": True,
                "schema": VISION_SCHEMA,
            },
        },
        max_tokens=2000,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    return VisionAnalysis(**data)


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

    system_prompt = f"""You are NutriMind AI, a friendly Korean nutrition coach.
Help users improve their eating habits with practical, actionable advice.
Always respond in Korean. Be encouraging but honest.
{meals_context}

Provide:
1. A helpful reply to the user's question
2. 1-3 specific actions they can take today
3. 1-2 meal or food suggestions if relevant"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "coach_response",
                "strict": True,
                "schema": COACH_SCHEMA,
            },
        },
        max_tokens=1000,
    )

    return json.loads(response.choices[0].message.content)
