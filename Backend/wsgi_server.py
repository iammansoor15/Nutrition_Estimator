from flask_cors import CORS
from server import app  # make sure your Flask instance is named `app`

# Apply CORS BEFORE serving
CORS(app, origins=[
    "http://localhost:5173",
    "https://nutrition-estimator-ufmf.onrender.com"
])

from waitress import serve
serve(app, host='0.0.0.0', port=5000)
