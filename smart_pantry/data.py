from datetime import datetime, timedelta
from typing import List, Dict
from .models import Ingredient, Recipe

# Mock Database for Ingredient Metadata
# Key: Ingredient Name
# Value: (Days to Expiry, Calories per unit, Cost per unit)
# Note: "unit" is somewhat arbitrary here (e.g., 100g, 1 egg, 1 liter)
MOCK_INGREDIENT_DB = {
    "Milk": (7, 60, 20),      # 7 days, 60 kcal/100ml, 20 NOK/L
    "Eggs": (14, 70, 4),      # 14 days, 70 kcal/egg, 4 NOK/egg
    "Flour": (180, 364, 15),  # 6 months, 364 kcal/100g, 15 NOK/kg
    "Chicken Breast": (4, 165, 120), # 4 days, 165 kcal/100g, 120 NOK/kg
    "Rice": (365, 130, 30),   # 1 year, 130 kcal/100g (cooked), 30 NOK/kg
    "Broccoli": (5, 34, 25),  # 5 days, 34 kcal/100g, 25 NOK/kg
    "Salmon": (3, 208, 200),  # 3 days, 208 kcal/100g, 200 NOK/kg
    "Potatoes": (14, 77, 15), # 14 days, 77 kcal/100g, 15 NOK/kg
    "Cheese": (30, 402, 100), # 30 days, 402 kcal/100g, 100 NOK/kg
    "Pasta": (365, 131, 20),  # 1 year, 131 kcal/100g, 20 NOK/kg
    "Tomato Sauce": (90, 82, 30), # 90 days, 82 kcal/100g, 30 NOK/jar
    "Ground Beef": (3, 250, 150), # 3 days, 250 kcal/100g, 150 NOK/kg
}

# Mock Recipe Database
# Ingredients quantities are in "units" corresponding to the DB
RECIPE_DB = [
    Recipe(
        name="Chicken & Rice",
        ingredients={"Chicken Breast": 2.0, "Rice": 1.5, "Broccoli": 1.0}, # units roughly 100g
        total_calories=550,
        instructions="Grill chicken, cook rice, steam broccoli."
    ),
    Recipe(
        name="Salmon Dinner",
        ingredients={"Salmon": 2.0, "Potatoes": 2.0, "Broccoli": 1.0},
        total_calories=600,
        instructions="Bake salmon and potatoes, serve with broccoli."
    ),
    Recipe(
        name="Pasta Bolognese",
        ingredients={"Pasta": 1.5, "Ground Beef": 1.5, "Tomato Sauce": 1.0, "Cheese": 0.5},
        total_calories=700,
        instructions="Cook pasta. Brown beef, add sauce. Serve with cheese."
    ),
    Recipe(
        name="Omelette",
        ingredients={"Eggs": 3.0, "Cheese": 0.5, "Milk": 0.5},
        total_calories=350,
        instructions="Whisk eggs and milk, cook in pan, add cheese."
    ),
    Recipe(
        name="Pancakes",
        ingredients={"Flour": 1.5, "Milk": 2.0, "Eggs": 2.0},
        total_calories=450,
        instructions="Mix ingredients, fry on pan."
    )
]

def ingest_vipps_receipt(receipt_lines: List[Dict]) -> List[Ingredient]:
    """
    Converts raw receipt lines (from Vipps API) into Ingredient objects.
    Enriches data with mock DB info.
    """
    ingredients = []
    today = datetime.now()

    for line in receipt_lines:
        name = line.get("name", "Unknown")
        # Simple fuzzy match or exact match

        matched_key = None
        for key in MOCK_INGREDIENT_DB:
            if key.lower() in name.lower():
                matched_key = key
                break

        if matched_key:
            shelf_life_days, calories, cost_per_unit = MOCK_INGREDIENT_DB[matched_key]

            # Parse quantity (Vipps uses strings often)
            try:
                qty_raw = line.get("quantity", "1")
                qty = float(qty_raw)
            except ValueError:
                qty = 1.0

            price_cents = line.get("totalAmount", 0)
            price = price_cents / 100.0 # Convert to currency units

            expiration = today + timedelta(days=shelf_life_days)

            ing = Ingredient(
                name=matched_key,
                expiration_date=expiration,
                calories_per_unit=calories, # Per "unit" defined in DB
                cost=price,
                quantity=qty,
                unit="unit"
            )
            ingredients.append(ing)
        else:
            # Item not recognized in our mock DB, skip or add generic
            pass

    return ingredients
