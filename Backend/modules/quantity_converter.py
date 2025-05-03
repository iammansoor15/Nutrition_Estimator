import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOOD_CATEGORIES_FILE = os.path.join(BASE_DIR, '../data/food_categories.json')

def extract_grams(weight_str):
    if isinstance(weight_str, str) and 'g' in weight_str.lower():
        return float(weight_str.lower().replace('g', '').strip())
    return None

def get_food_unit_and_scaled_nutrients(food_type, totals, total_weight):
    try:
        with open(FOOD_CATEGORIES_FILE, 'r') as file:
            data = json.load(file)

        food_categories = data.get("food_categories", [])

        unit = None
        category_weight = None

        for category in food_categories:
            if category["name"].lower() == food_type.lower():
                unit = category["unit"]
                weight_str = category["weight"]
                category_weight = extract_grams(weight_str)

                if not category_weight:
                    return {"error": f"Invalid weight format: {weight_str}"}

                if total_weight == 0:
                    return {"error": "Total weight of ingredients is zero. Cannot scale."}

                scaling_factor = category_weight / total_weight
                nutrition_per_unit = {
                    nutrient: round(value * scaling_factor, 2)  
                    for nutrient, value in totals.items()
                    if isinstance(value, (int, float))
                }

                return {
                    "unit": unit,
                    "category_weight": category_weight,
                    f"estimated_nutrition_per_{category_weight}g_or_{unit.lower()}": {
                        "nutrition": nutrition_per_unit
                    }
                }

        if unit is None or category_weight is None:
            return {"error": f"Food type '{food_type}' not found in food categories."}

    except Exception as e:
        return {"error": str(e)}