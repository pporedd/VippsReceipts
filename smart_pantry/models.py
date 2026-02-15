from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from enum import Enum

class ActivityLevel(Enum):
    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    VERY_ACTIVE = 1.725
    EXTRA_ACTIVE = 1.9

@dataclass
class Ingredient:
    name: str
    expiration_date: datetime
    calories_per_unit: float
    cost: float
    quantity: float
    unit: str

    def __lt__(self, other):
        # Comparison logic for the Min-Heap (priority queue)
        # Ingredients expiring sooner are "smaller" (higher priority)
        return self.expiration_date < other.expiration_date

@dataclass
class Recipe:
    name: str
    ingredients: Dict[str, float]  # Name -> Quantity needed
    total_calories: float
    instructions: str = ""

@dataclass
class UserProfile:
    age: int
    weight_kg: float
    height_cm: float
    gender: str # 'male' or 'female'
    activity_level: ActivityLevel
