import pandas as pd
from ingredient_matching import match_ingredient

def get_specific_nutrients(ingredients, nutrition_db, nutrition_db_embeddings):
    nutrients_columns = [
        'energy_kcal', 'carb_g', 'protein_g', 'fat_g', 'fibre_g',
        'calcium_mg', 'iron_mg', 'sodium_mg', 'potassium_mg'
    ]
    nutrients_data = []
    total_weight = 0  # Track total ingredient weight

    for ingredient, details in ingredients.items():
        quantity = details.get('quantity_grams')
        if quantity is None:
            print(f"Skipping {ingredient} due to missing quantity.")
            continue

        nutrition_row, matched_name = match_ingredient(ingredient)
        if nutrition_row is not None:
            scaled = nutrition_row[nutrients_columns] * (quantity / 100)
            scaled['fetched_ingredient'] = ingredient
            scaled['matched_ingredient'] = matched_name
            scaled['quantity_g'] = quantity
            nutrients_data.append(scaled)
            total_weight += quantity  # Add to total weight

    nutrients_df = pd.DataFrame(nutrients_data)
    print("Total nutrients data:")
    print(nutrients_df)

    totals = None
    if not nutrients_df.empty:
        totals = nutrients_df[nutrients_columns].sum().round(0).astype(int)
        print("\nTotal nutrients:")
        print(totals)
    else:
        print("\nNo nutrient data found to calculate totals.")
    
    return totals, nutrients_df, total_weight  # Return total weight for scaling