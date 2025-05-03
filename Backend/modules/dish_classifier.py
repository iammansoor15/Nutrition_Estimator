import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from ingredient_normalisation import normalize_ingredient_name  # Import normalization directly

# Debugging the working directory
print("Current Working Directory:", os.getcwd())

# Step 1: Load data from JSON file
file_path = os.path.join(os.path.dirname(__file__), '../data/item_catergorisation.json')  # Adjust the path as needed
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

with open(file_path, 'r') as f:
    food_category_data = json.load(f)

# Step 2: Prepare data for training
X = []  # Food item names
y = []  # Categories

# Extract category names from JSON and use them as labels
categories = food_category_data["food_category_data"]

# Populate training data
for category, items in categories.items():
    for item in items:
        X.append(item)
        y.append(category)

# Step 3: Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Define a pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())  # You can replace with LogisticRegression or SVC
])

# Step 5: Train the model
pipeline.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = pipeline.predict(X_test)

# Step 7: Predict new item with normalization
def predict_category(item_name):
    normalized_item = normalize_ingredient_name(item_name)  # Normalize the item name
    return pipeline.predict([normalized_item])[0]