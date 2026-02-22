import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from smart_pantry.models import UserProfile, ActivityLevel, Ingredient
from smart_pantry.data import ingest_vipps_receipt
from smart_pantry.optimizer import PantryManager, MealPlanner
from smart_pantry.calculator import calculate_tdee

app = Flask(__name__)
CORS(app) # Enable CORS for frontend

# Mock Data Persistence (In-memory for now)
current_user = UserProfile(30, 75.0, 180.0, "male", ActivityLevel.MODERATELY_ACTIVE)
pantry_manager = PantryManager()

# Simulate pre-loading pantry
initial_receipt = [
    {"name": "Chicken Breast", "quantity": "4", "totalAmount": 48000},
    {"name": "Rice", "quantity": "2", "totalAmount": 6000},
    {"name": "Broccoli", "quantity": "5", "totalAmount": 12500},
    {"name": "Milk", "quantity": "2", "totalAmount": 4000},
    {"name": "Eggs", "quantity": "6", "totalAmount": 2400},
    {"name": "Flour", "quantity": "1", "totalAmount": 1500},
    {"name": "Salmon", "quantity": "2", "totalAmount": 40000},
    {"name": "Potatoes", "quantity": "3", "totalAmount": 4500},
]
for item in ingest_vipps_receipt(initial_receipt):
    pantry_manager.add_ingredient(item)


@app.route('/api/login', methods=['POST'])
def login():
    """Simulates Vipps Login."""
    # In real app: Redirect to Vipps, get token, fetch user info
    return jsonify({
        "status": "success",
        "user": {
            "name": "Test User",
            "age": current_user.age,
            "tdee": calculate_tdee(current_user)
        }
    })

@app.route('/api/pantry', methods=['GET'])
def get_pantry():
    """Returns pantry items sorted by expiration urgency."""
    ingredients = []
    # Dump heap to list without removing items
    # Note: Using private access for prototype speed, ideally use getter
    for ing in pantry_manager.ingredients_heap:
        days_left = (ing.expiration_date - datetime.now()).days
        ingredients.append({
            "name": ing.name,
            "days_left": days_left,
            "quantity": ing.quantity,
            "unit": ing.unit,
            "calories": ing.calories_per_unit,
            "image_url": f"https://source.unsplash.com/200x200/?{ing.name.replace(' ', ',')}" # Placeholder
        })

    # Sort by urgency (days left)
    ingredients.sort(key=lambda x: x['days_left'])
    return jsonify(ingredients)

@app.route('/api/swipe', methods=['POST'])
def swipe_action():
    """
    Records a user's swipe action (Left/Right) for an ingredient.
    Future: Use this data for Federated Learning.
    """
    data = request.json
    item_name = data.get('item_name')
    action = data.get('action') # 'keep' (right) or 'discard' (left)

    # Logic: Maybe mark as 'consumed' if discarded?
    # For now, just log it.
    print(f"User swiped {action} on {item_name}")

    return jsonify({"status": "recorded", "action": action, "item": item_name})

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    """Generates a meal plan based on constraints."""
    data = request.json
    budget = float(data.get('budget', 500.0))
    # Update user constraints if needed (e.g. calorie target overrides TDEE)

    planner = MealPlanner(pantry_manager)
    plan = planner.suggest_meals(current_user, daily_budget=budget)

    if "error" in plan:
        return jsonify({"status": "error", "message": plan["error"]}), 400

    return jsonify({
        "status": "success",
        "plan": plan
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
