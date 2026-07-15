"""CNN food classification stub.

Phase 1 MVP uses a mock classifier. Replace with EfficientNet-B3 / MobileNetV3
when model weights are available.
"""

import random

from app.models.schemas import CNNResult

KOREAN_FOODS = [
    ("비빔밥", "korean"),
    ("김치찌개", "korean"),
    ("불고기", "korean"),
    ("삼겹살", "korean"),
    ("떡볶이", "korean"),
    ("김밥", "korean"),
    ("된장찌개", "korean"),
    ("치킨", "fast_food"),
    ("라면", "korean"),
    ("샐러드", "healthy"),
]

GENERAL_FOODS = [
    ("Pizza", "western"),
    ("Burger", "fast_food"),
    ("Pasta", "western"),
    ("Sushi", "japanese"),
    ("Steak", "western"),
    ("Sandwich", "western"),
    ("Salad", "healthy"),
    ("Rice Bowl", "asian"),
]


def classify_food(image_bytes: bytes) -> CNNResult:
    """Mock CNN classification based on image size hash for consistency."""
    seed = sum(image_bytes[:1000]) if image_bytes else random.randint(0, 9999)
    rng = random.Random(seed)
    pool = KOREAN_FOODS + GENERAL_FOODS
    name, category = rng.choice(pool)
    confidence = round(rng.uniform(0.72, 0.96), 2)
    return CNNResult(food_name=name, confidence=confidence, category=category)
