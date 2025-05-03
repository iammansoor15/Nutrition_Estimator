import json
from pathlib import Path

# Path to the household units JSON file
DATA_FILE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'household_measurements.json'

def load_household_units():
    """
    Loads the household units mapping from the JSON file.

    :return: A list of household unit mappings.
    """
    with open(DATA_FILE_PATH, 'r') as file:
        return json.load(file)["units"]

def convert_to_household_units(quantity_in_grams):
    """
    Converts the given quantity in grams to a more user-friendly household unit.

    :param quantity_in_grams: The quantity in grams to be converted.
    :return: A string representing the quantity in household units (e.g., "1 Cup or Katori").
    """
    # Load the household units mapping
    household_units = load_household_units()

    # Find the most appropriate household unit
    best_match = None
    for unit in household_units:
        if quantity_in_grams >= unit["value"]:
            best_match = unit

    if best_match:
        quantity_in_units = quantity_in_grams / best_match["value"]
        return f"{quantity_in_units:.2f} {best_match['name']}"

    # Default to grams if no suitable match is found
    return f"{quantity_in_grams:.2f} grams"