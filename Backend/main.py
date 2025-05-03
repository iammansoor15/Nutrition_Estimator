import json
import os
from pathlib import Path
import sys
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

# Set base and modules directory
BASE_DIR = Path(__file__).resolve().parent
MODULES_DIR = BASE_DIR / 'modules'
sys.path.append(str(MODULES_DIR))

# Import custom modules
from fetch_ingredients import fetch_ingredients
from nutrient_scaling import get_specific_nutrients
from dish_classifier import predict_category
from quantity_converter import get_food_unit_and_scaled_nutrients
from household_units_mapping import convert_to_household_units

# Define path to the nutrition database CSV
DATA_FILE_PATH = BASE_DIR / './data/nutrition_database.csv'

# Load nutrition database
nutrition_db = pd.read_csv(DATA_FILE_PATH)
nutrition_db['food_name_cleaned'] = nutrition_db['food_name'].astype(str).str.lower().str.strip()

# Load sentence transformer model
nlp_model = SentenceTransformer('all-MiniLM-L6-v2')
nutrition_db['food_name_embeddings'] = list(
    nlp_model.encode(nutrition_db['food_name_cleaned'], convert_to_tensor=True)
)
nutrition_db_embeddings = torch.stack(list(nutrition_db['food_name_embeddings']))

# Save data to JSON
def save_to_json(data, dish_name):
    output_dir = os.path.join(BASE_DIR, 'Outputs')
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{dish_name.replace(' ', '_').lower()}.json"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Output successfully saved to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Dish name not provided as argument.")
        sys.exit(1)

    dish_name = sys.argv[1].strip()
    print(f"Processing dish: {dish_name}")

    ingredients = fetch_ingredients(dish_name)
    if not ingredients:
        print("No ingredients found. Exiting...")
        sys.exit(1)

    parsed_ingredients = []
    for name, details in ingredients.items():
        quantity = details.get('quantity_grams')
        quantity_str = convert_to_household_units(quantity) if quantity else "N/A"
        parsed_ingredients.append({
            "ingredient": name,
            "quantity": quantity_str
        })

    dish_type = predict_category(dish_name)

    totals, nutrient_data, total_weight = get_specific_nutrients(
        {name: {'quantity_grams': details.get('quantity_grams', 0)} for name, details in ingredients.items()},
        nutrition_db,
        nutrition_db_embeddings
    )

    per_unit_nutrition = get_food_unit_and_scaled_nutrients(dish_type, totals, total_weight)
 
    output_data = {
        'dish_name': dish_name,
        'dish_type': dish_type,
        'ingredients_used': parsed_ingredients,
        **per_unit_nutrition
    }

    save_to_json(output_data, dish_name)
