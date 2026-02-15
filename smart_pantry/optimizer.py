import heapq
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from .models import Ingredient, Recipe, UserProfile
from .calculator import calculate_tdee
from .data import RECIPE_DB

class PantryManager:
    def __init__(self):
        self.ingredients_heap = [] # Min-Heap based on expiration
        self.inventory = {} # Map name -> List[Ingredient]

    def add_ingredient(self, ingredient: Ingredient):
        heapq.heappush(self.ingredients_heap, ingredient)
        if ingredient.name not in self.inventory:
            self.inventory[ingredient.name] = []
        self.inventory[ingredient.name].append(ingredient)

    def get_all_ingredients(self):
        return self.ingredients_heap

    def get_ingredient_urgency(self, name: str) -> float:
        """
        Returns a score based on how close the item is to expiring.
        Higher score = more urgent.
        """
        if name not in self.inventory or not self.inventory[name]:
            return 0.0

        # Find the batch expiring soonest
        best_ing = min(self.inventory[name], key=lambda x: x.expiration_date)

        days_left = (best_ing.expiration_date - datetime.now()).days
        # Formula: 100 / (days_left + 1). If expired (negative), massive urgency.
        if days_left < 0:
            return 1000.0 # Expired/Expiring today
        if days_left == 0:
            return 500.0
        return 100.0 / days_left

    def has_ingredient(self, name: str, qty_needed: float) -> bool:
        if name not in self.inventory:
            return False
        total_qty = sum(i.quantity for i in self.inventory[name])
        return total_qty >= qty_needed

    def get_unit_cost(self, name: str) -> float:
        if name in self.inventory and self.inventory[name]:
            ing = self.inventory[name][0]
            if ing.quantity > 0:
                return ing.cost / ing.quantity
        return 0.0

class MealPlanner:
    def __init__(self, pantry: PantryManager):
        self.pantry = pantry
        self.recipes = RECIPE_DB

    def suggest_meals(self, user: UserProfile, daily_budget: float, meals_per_day: int = 3) -> Dict:
        """
        Selects meals to maximize pantry usage (urgency) within calorie and budget constraints.
        """
        tdee = calculate_tdee(user)

        # 1. Pre-calculate metrics for each recipe
        # We only consider recipes we can actually make (or mostly make)
        candidates = []

        for r in self.recipes:
            can_make = True
            cost = 0.0
            urgency = 0.0

            for ing_name, qty in r.ingredients.items():
                if not self.pantry.has_ingredient(ing_name, qty):
                    can_make = False
                    break

                # Calculate cost and urgency
                unit_cost = self.pantry.get_unit_cost(ing_name)
                cost += unit_cost * qty
                urgency += self.pantry.get_ingredient_urgency(ing_name)

            if can_make:
                candidates.append({
                    "recipe": r,
                    "urgency": urgency,
                    "cost": cost,
                    "calories": r.total_calories
                })

        # If no recipes are possible, return empty
        if not candidates:
            return {"error": "No feasible recipes found with current pantry."}

        # 2. Dynamic Programming / Recursion with Memoization
        # State: (meals_eaten, current_cals_int, current_cost_int)
        # We want to find a combination of indices from `candidates`

        # To make memoization work, we need integer keys.
        # Cost -> cents (int)
        # Calories -> int

        memo = {}

        # limit recursion depth
        MAX_CALS = int(tdee * 1.1) # Allow 10% buffer? Or strict? Let's be strict as per "limit"
        MAX_COST = int(daily_budget * 100) # Cents

        def solve(count, current_cals, current_cost):
            state = (count, current_cals, current_cost)
            if state in memo:
                return memo[state]

            if count == meals_per_day:
                return (0, []) # Base case: 0 extra urgency, empty list of additional meals

            best_urgency = -1.0
            best_combo = None

            # Try adding every possible candidate recipe
            # Note: We can repeat recipes (e.g. eat leftovers)
            for item in candidates:
                r_cals = int(item["calories"])
                r_cost = int(item["cost"] * 100)
                r_urgency = item["urgency"]

                if current_cals + r_cals <= MAX_CALS and current_cost + r_cost <= MAX_COST:
                    res_urgency, res_list = solve(count + 1, current_cals + r_cals, current_cost + r_cost)

                    if res_urgency != -1: # Valid path
                        total_urgency = r_urgency + res_urgency
                        if total_urgency > best_urgency:
                            best_urgency = total_urgency
                            best_combo = [item] + res_list

            if best_urgency == -1.0 and count > 0:
                # If we can't fill ALL meals, but we have some, is that valid?
                # For this logic, let's assume we MUST fill 'meals_per_day' slots if possible.
                # If strict, return -1. If loose, return 0.
                # Let's try to be strict.
                 memo[state] = (-1, [])
            else:
                 memo[state] = (best_urgency, best_combo)

            return memo[state]

        # Start search
        score, plan = solve(0, 0, 0)

        if score == -1 or plan is None:
             # Try fallback: find BEST single meal or whatever fits
             return {"error": "Cannot find a full meal plan satisfying all constraints."}

        # Format output
        result = {
            "total_calories": sum(item["calories"] for item in plan),
            "total_cost": sum(item["cost"] for item in plan),
            "total_urgency_score": score,
            "meals": [item["recipe"].name for item in plan]
        }
        return result
