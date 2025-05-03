# Dish Nutrition Estimator

This repository provides a modular Python-based solution for estimating the nutritional content of dishes based on their ingredients. The application integrates AI-powered ingredient fetching, ingredient normalization, household unit conversion, and nutrient scaling to produce detailed nutritional estimates for dishes. It includes both backend and frontend components, with a React-based user interface for ease of use. The backend processes the dish information and generates a JSON file, which is then displayed on the frontend.

---

## Features

- **AI-Powered Ingredient Fetching**: Automatically fetches ingredients for a dish using a generative AI model.
- **Ingredient Normalization**: Cleans and normalizes ingredient names for consistency.
- **Ingredient Matching**: Matches normalized ingredient names to a nutrition database.
- **Nutrient Scaling**: Scales nutrients based on ingredient quantities.
- **Dish Classification**: Classifies dishes into categories for better nutrient scaling.
- **Household Unit Conversion**: Converts ingredient quantities into user-friendly household units (e.g., cups, teaspoons).
- **Dynamic Output**: Produces JSON files containing parsed ingredients, dish type, and nutritional estimates.
- **React Frontend**: Displays the JSON output in a user-friendly interface for searching and viewing dish information.

---

## Assumptions Made

1. **AI Model**: The generative AI model (Google Generative AI - `gemini-2.5`) provides valid, Python-dictionary formatted responses for ingredient queries.
2. **Nutrient Database**: The `nutrition_database.csv` contains accurate and comprehensive nutritional information for all possible ingredients.
3. **Dish Classification**: The `item_catergorisation.json` file contains all necessary dish categories and their corresponding food items for classification.
4. **Household Units**: The `household_measurements.json` file includes all commonly used household units and their equivalences in grams.
5. **Error Handling**: Graceful handling of missing or invalid data is implemented, and appropriate error messages are returned.
6. **Outputs**: Outputs are stored in the `outputs` folder, with file names dynamically generated from the input dish name (e.g., `dish_name.json`) and displayed in the frontend.

---

## Approach to Modularization

Modularization is achieved by decoupling the application into logically independent modules, each responsible for a specific task:

### Backend Modules

1. **`fetch_ingredients.py`**
   - Fetches the list of ingredients for a given dish using AI.
   - Ensures the response is parsed into a valid Python dictionary.
   - Handles errors related to invalid or empty responses.

2. **`ingredient_normalisation.py`**
   - Cleans and normalizes ingredient names using:
     - Regular expressions for cleaning unwanted characters.
     - WordNet for finding synonyms of ingredient names.

3. **`ingredient_matching.py`**
   - Matches normalized ingredient names to entries in a nutrition database using:
     - Sentence embeddings (`SentenceTransformer`).
     - Cosine similarity for finding the best match.

4. **`ingredient_scaling.py`**
   - Scales the nutrient values for a dish based on the quantity of each ingredient.
   - Uses the matching logic from `ingredient_matching.py` and calculates totals for nutrients like calories, protein, carbs, etc.

5. **`dish_classifier.py`**
   - Classifies dishes into categories (e.g., "Veg Gravy", "Snacks") using a Naive Bayes model.
   - Uses TF-IDF vectorization for feature extraction.
   - Supports normalization of input dish names for consistency.

6. **`quantity_converter.py`**
   - Converts ingredient quantities into user-friendly household units (e.g., "2 cups", "3 teaspoons").
   - Dynamically scales nutrients based on dish weight and specific household unit sizes.

7. **`household_units_mapping.py`**
   - Loads household unit definitions from `household_measurements.json`.
   - Provides utility functions to convert quantities in grams to household units.

8. **`main.py`**
   - Integrates all modules into a single workflow:
     1. Fetches ingredients for a dish.
     2. Normalizes and matches ingredients.
     3. Scales nutrients.
     4. Converts quantities to household units.
     5. Classifies the dish type.
     6. Saves the output as a JSON file.

---

## Folder Structure

```
Dish-Nutrition-Estimator/
│
├── backend/                          # Backend folder
│   ├── main.py                       # Entry point for the backend application
│   ├── modules/                      # Contains all modular scripts
│   │   ├── fetch_ingredients.py      # Fetches ingredients using AI
│   │   ├── ingredient_normalisation.py # Normalizes ingredient names
│   │   ├── ingredient_matching.py    # Matches ingredients to nutrition database
│   │   ├── ingredient_scaling.py     # Scales nutrient values
│   │   ├── dish_classifier.py        # Classifies dishes
│   │   ├── quantity_converter.py     # Converts quantities to household units
│   │   ├── household_units_mapping.py # Maps grams to household units
│   │
│   ├── data/                         # Contains static data files
│   │   ├── nutrition_database.csv    # Nutrition database
│   │   ├── item_catergorisation.json # Dish categories and food items
│   │   ├── food_categories.json      # Food categories for scaling
│   │   ├── household_measurements.json # Household measurements in grams
│   │
│   ├── outputs/                      # Contains output JSON files
│   │   └── <dish_name>.json          # Output for a specific dish
│   │
│   ├── server.py                     # Flask backend server
│   ├── wsgi_server.py                # Production-ready server using Waitress
│   └── README.md                     # Documentation for the backend
│
├── frontend/                         # Frontend folder
│   ├── react/                        # React folder
│   │   ├── public/                   # Public assets
│   │   ├── src/                      # Source code
│   │   │   ├── pages/                # Pages directory
│   │   │   │   ├── Home.jsx          # Home page component
│   │   │   ├── App.jsx               # Main React component
│   │   │   ├── index.js              # Entry point
│   │
│   ├── README.md                     # Documentation for the frontend
└── README.md                         # Main documentation for the project
```

---

## How to Run

### Backend

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<username>/Dish-Nutrition-Estimator.git
   cd Backend
   ```

2. **Install Dependencies**:
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install required libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Backend Server**:
   ```bash
   python wsgi_server.py
   ```

The backend will start running on `http://127.0.0.1:5000`.

### Frontend

1. **Navigate to the Frontend Folder**:
   ```bash
   cd Frontend/
   ```

2. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```

3. **Start the React Development Server**:
   ```bash
   npm start
   ```

The frontend will be available on `http://localhost:5173`.

---

## Input/Output

### Input

- Dish Name: The user provides the name of the dish (e.g., "Palak Paneer", "Chicken Biryani") through the React frontend.

### Output

- A JSON file is generated in the `outputs` folder with the following structure:

```json
{
    "dish_name": "Palak Paneer",
    "dish_type": "Veg Gravy",
    "ingredients_used": [
        { "ingredient": "Spinach", "quantity": "3.33 Cup or Katori" },
        { "ingredient": "Paneer", "quantity": "1.33 Cup or Katori" },
        { "ingredient": "Onions", "quantity": "1.00 Cup or Katori" }
    ],
    "unit": "Katori",
    "weight_per_unit": "150.0g",
    "estimated_nutrition_per_200ml_katori": {
        "energy_kcal": 230,
        "carb_g": 13,
        "protein_g": 9,
        "fat_g": 15
    }
}
```

The React frontend displays this JSON data in a user-friendly format.

---

## Dependencies

- Python 3.8 or higher
- Flask
- Flask-CORS
- Waitress
- pandas
- torch
- sentence-transformers
- nltk
- scikit-learn
- google-generativeai
- React
- Node.js (for the frontend)

---

