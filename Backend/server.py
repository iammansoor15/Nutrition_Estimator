import logging
from flask import Flask, jsonify, request
import os
import json
import subprocess

app = Flask(__name__)

CORS(app)

# Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define required fields
REQUIRED_FIELDS = [
    "dish_name", "dish_type", "ingredients_used", "unit", "category_weight"
]

@app.route('/api/get_dish_info/<dish_name>', methods=['GET'])
def get_dish_info(dish_name):
    """
    Endpoint to get dish information. If the data file exists and is valid,
    it returns the data; otherwise, it runs the Python script to generate it.
    """
    if not dish_name:
        return jsonify({"error": "Missing 'dish_name' query param"}), 400

    # Resolve file paths
    root_dir = os.path.abspath(os.path.dirname(__file__))  # Root directory
    output_dir = os.path.join(root_dir, "Outputs")
    file_name = f"{dish_name.replace(' ', '_').lower()}.json"
    file_path = os.path.join(output_dir, file_name)

    logger.info(f"Looking for file: {file_path}")

    def send_or_generate():
        if not os.path.exists(output_dir):
            # Create the directory if it doesn't exist
            try:
                os.makedirs(output_dir)
                logger.info(f"Created missing directory: {output_dir}")
            except Exception as e:
                logger.error(f"Failed to create directory {output_dir}: {e}")
                return jsonify({"error": f"Failed to create directory: {e}"}), 500

        if os.path.exists(file_path):
            # File exists, read it
            logger.info(f"File {file_name} found.")
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON file {file_name}: {e}")
                    return jsonify({"error": f"Invalid JSON file: {e}"}), 500
            
            # Check if all required fields exist in the data
            missing_keys = [key for key in REQUIRED_FIELDS if key not in data]
            if not missing_keys:
                logger.info("All required fields are found in the data.")
                return jsonify(data)  # Return the JSON if all keys are present
            else:
                logger.error(f"Missing keys in the data: {', '.join(missing_keys)}")
                return run_python_script(dish_name)

        else:
            logger.info(f"File {file_name} not found. Running the Python script to generate it.")
            # If the file doesn't exist, run the script to generate it
            return run_python_script(dish_name)

    return send_or_generate()

def run_python_script(dish_name):
    """
    Runs the Python script to generate dish information and returns the result.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))  # Root directory
    main_script_path = os.path.join(root_dir, "main.py")  # Path to main.py
    output_dir = os.path.join(root_dir, "Outputs")
    file_name = f"{dish_name.replace(' ', '_').lower()}.json"
    file_path = os.path.join(output_dir, file_name)

    try:
        if not os.path.exists(main_script_path):
            raise FileNotFoundError(f"main.py not found at {main_script_path}")

        logger.info(f"Executing command: python {main_script_path} {dish_name}")
        process = subprocess.Popen(
            ["python", main_script_path, dish_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=root_dir  # Run the command from the root directory
        )
        stdout, stderr = process.communicate()

        logger.info(f"Python stdout: {stdout.decode('utf-8')}")
        if stderr:
            logger.error(f"Python stderr: {stderr.decode('utf-8')}")

        if process.returncode == 0 and os.path.exists(file_path):
            logger.info(f"File {file_name} created successfully.")
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON file {file_name}: {e}")
                    return jsonify({"error": f"Invalid JSON file: {e}"}), 500

            # Check if all required fields exist in the generated data
            missing_keys = [key for key in REQUIRED_FIELDS if key not in data]
            if not missing_keys:
                logger.info("All required fields are found in the generated data.")
                return jsonify(data)
            else:
                logger.error(f"Missing keys in the generated data: {', '.join(missing_keys)}")
                return jsonify({"error": f"Missing keys: {', '.join(missing_keys)}"}), 500

        else:
            logger.error(f"JSON file {file_name} not created successfully.")
            return jsonify({"error": "JSON file not created"}), 500

    except Exception as e:
        logger.error(f"Failed to start Python script: {e}")
        return jsonify({"error": f"Failed to run main.py: {e}"}), 500

