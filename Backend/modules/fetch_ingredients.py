import google.generativeai as genai
import ast
import os

# Configure the GenAI API
genai.configure(api_key='AIzaSyCuQoItehlMh51yKzTc9iy_8FuM47Dlcgw')
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

def fetch_ingredients(dish_name):
    """
    Fetch ingredients for a given dish name using the AI model.
    
    Args:
        dish_name (str): The name of the dish for which ingredients are being fetched.
    
    Returns:
        dict: A dictionary where keys are ingredient names, and values are dictionaries
              containing the quantity in grams and scientific names.
    """
    prompt = (
        f"Give me complete ingredients to make {dish_name}. Keys are the ingredient names in English, "
        "and the values are dictionaries containing the quantity in grams (as an integer) "
        "and the scientific name. Only return a valid Python dictionary. "
        "Do not return JSON. Do not wrap in quotes, markdown, or code blocks. Return only the dict."
    )
    
    try:
        # Generate content from the AI model
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("No response from the AI model.")
        
        raw_response = response.text.strip()

        # Clean the response by removing backticks and language annotations (if any)
        if raw_response.startswith("```") and raw_response.endswith("```"):
            raw_response = raw_response.strip("```").strip()
            # If the cleaned string starts with a language annotation (e.g., "python"), remove it
            if raw_response.startswith("python"):
                raw_response = raw_response[len("python"):].strip()

        # Safely parse the response using ast.literal_eval
        ingredients = ast.literal_eval(raw_response)
        if isinstance(ingredients, dict):
            print("Success: fetch_ingredients.py")  # Success message
            return ingredients
        else:
            raise ValueError("Response is not a valid Python dictionary.")
    except (SyntaxError, ValueError) as e:
        print(f"Parsing error: {e}")
        print(f"Problematic Response: {raw_response}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    dish_name = input("Enter a dish name: ").strip()  # Prompt for dish name
    ingredients = fetch_ingredients(dish_name)
    print("Parsed Ingredients:", ingredients)