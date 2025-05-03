from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
import re
from ingredient_normalisation import normalize_ingredient_name

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE_PATH = BASE_DIR / '../data/nutrition_database.csv'

# Load Nutrition Database
nutrition_db = pd.read_csv(DATA_FILE_PATH)
nutrition_db['food_name_cleaned'] = nutrition_db['food_name'].astype(str).str.lower().str.strip()

# Load SentenceTransformer model
nlp_model = SentenceTransformer('all-MiniLM-L6-v2')
nutrition_db['food_name_embeddings'] = list(
    nlp_model.encode(nutrition_db['food_name_cleaned'], convert_to_tensor=True)
)
nutrition_db_embeddings = torch.stack(list(nutrition_db['food_name_embeddings']))

def parse_quantity(value):
    try:
        value = re.sub(r'[^\d.]', '', str(value))  # Remove non-numeric characters
        return float(value)
    except ValueError:
        print(f"Warning: Could not parse quantity: {value}")
        return None

def match_ingredient(ingredient_name):
    normalized_name = normalize_ingredient_name(ingredient_name)
    embedding = nlp_model.encode(normalized_name, convert_to_tensor=True)
    similarities = util.cos_sim(embedding, nutrition_db_embeddings)
    best_match_idx = similarities.argmax().item()
    best_score = similarities[0, best_match_idx].item()

    if best_score > 0.6:
        best_match = nutrition_db.iloc[best_match_idx]
        return best_match, best_match['food_name']
    else:
        print(f"Warning: No confident match found for ingredient: {ingredient_name}")
        return None, None