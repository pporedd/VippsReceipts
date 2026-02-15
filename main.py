from datetime import datetime
from smart_pantry.models import UserProfile, ActivityLevel
from smart_pantry.data import ingest_vipps_receipt
from smart_pantry.optimizer import PantryManager, MealPlanner
from smart_pantry.calculator import calculate_tdee

def main():
    print("--- Smart Pantry & Meal Planner ---")

    # 1. Setup User
    user = UserProfile(
        age=30,
        weight_kg=75.0,
        height_cm=180.0,
        gender="male",
        activity_level=ActivityLevel.MODERATELY_ACTIVE
    )
    tdee = calculate_tdee(user)
    print(f"User TDEE: {tdee:.0f} kcal/day")

    # 2. Simulate Vipps Receipt Data
    # We simulate a mix of items.
    # Note: Chicken expires in 4 days (high urgency).
    # Salmon expires in 3 days (higher urgency).
    receipt_data = [
        {"name": "Chicken Breast", "quantity": "4", "totalAmount": 48000}, # 4 units
        {"name": "Rice", "quantity": "2", "totalAmount": 6000},
        {"name": "Broccoli", "quantity": "5", "totalAmount": 12500},
        {"name": "Milk", "quantity": "2", "totalAmount": 4000},
        {"name": "Eggs", "quantity": "6", "totalAmount": 2400},
        {"name": "Flour", "quantity": "1", "totalAmount": 1500},
        {"name": "Salmon", "quantity": "2", "totalAmount": 40000},
        {"name": "Potatoes", "quantity": "3", "totalAmount": 4500},
    ]

    # 3. Ingest to Pantry
    ingredients = ingest_vipps_receipt(receipt_data)
    pantry = PantryManager()
    for ing in ingredients:
        pantry.add_ingredient(ing)

    print(f"\nPantry Loaded with {len(ingredients)} items.")
    print("Top expiring items:")
    # Peek at heap by sorting a copy
    sorted_pantry = sorted(pantry.get_all_ingredients())
    for i in sorted_pantry[:3]:
        days = (i.expiration_date - datetime.now()).days
        print(f" - {i.name}: expires in {days} days")

    # 4. Plan Meals
    # We assume 'meals_per_day=3'.
    # Chicken & Rice = 550kcal, Urgency from Chicken(4d) + Broccoli(5d)
    # Salmon Dinner = 600kcal, Urgency from Salmon(3d) + Potatoes(14d) + Broccoli(5d) -> Higher urgency!

    planner = MealPlanner(pantry)
    budget = 1000.0 # High budget to ensure we find a solution first

    print(f"\nGenerating Meal Plan (Budget: {budget} NOK)...")
    plan = planner.suggest_meals(user, daily_budget=budget, meals_per_day=3)

    if "error" in plan:
        print(f"Error: {plan['error']}")
    else:
        print("\n--- Suggested Meal Plan ---")
        for idx, meal_name in enumerate(plan["meals"]):
            print(f"Meal {idx+1}: {meal_name}")

        print(f"\nTotal Calories: {plan['total_calories']} kcal (Target: {tdee:.0f})")
        print(f"Total Cost: {plan['total_cost']:.2f} NOK (Budget: {budget:.2f})")
        print(f"Urgency Score: {plan['total_urgency_score']:.2f}")

if __name__ == "__main__":
    main()
