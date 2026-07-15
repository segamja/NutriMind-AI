from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PortionItem(BaseModel):
    name: str
    amount_g: float
    confidence: float = Field(ge=0, le=1)


class NutritionInfo(BaseModel):
    calories: float
    protein: float
    fat: float
    carbohydrates: float
    fiber: float = 0
    sugar: float = 0
    sodium: float = 0
    calcium: float = 0
    iron: float = 0
    potassium: float = 0


class MealScore(BaseModel):
    overall: int = Field(ge=0, le=100)
    calories: int = Field(ge=0, le=100)
    protein: int = Field(ge=0, le=100)
    fat: int = Field(ge=0, le=100)
    carbohydrates: int = Field(ge=0, le=100)
    sugar: int = Field(ge=0, le=100)
    sodium: int = Field(ge=0, le=100)
    fiber: int = Field(ge=0, le=100)


class CNNResult(BaseModel):
    food_name: str
    confidence: float = Field(ge=0, le=1)
    category: str = "general"


class VisionAnalysis(BaseModel):
    food_name: str
    description: str
    ingredients: list[str]
    cooking_method: str
    portions: list[PortionItem]
    nutrition: NutritionInfo
    health_score: MealScore
    actions: list[str] = Field(description="Recommended next actions for the user")


class ScanResponse(BaseModel):
    cnn: CNNResult
    vision: VisionAnalysis
    scan_id: str | None = None


class MealRecord(BaseModel):
    id: str
    food_name: str
    image_url: str | None = None
    nutrition: NutritionInfo
    health_score: int
    ingredients: list[str]
    actions: list[str]
    created_at: datetime


class MealCreate(BaseModel):
    food_name: str
    image_url: str | None = None
    nutrition: NutritionInfo
    health_score: int
    ingredients: list[str]
    actions: list[str]


class CoachMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class CoachRequest(BaseModel):
    message: str
    history: list[CoachMessage] = []
    today_meals: list[MealRecord] = []


class CoachResponse(BaseModel):
    reply: str
    actions: list[str] = []
    suggestions: list[str] = []


class DashboardStats(BaseModel):
    total_meals: int
    avg_calories: float
    avg_protein: float
    avg_health_score: float
    today_calories: float
    today_protein: float
    weekly_calories: list[dict[str, float | str]]


class WeeklyReport(BaseModel):
    period: str
    total_meals: int
    habit_analysis: str
    nutrient_analysis: str
    avg_health_score: float
    improvements: list[str]
    next_week_goals: list[str]
    summary: str
