from flask_cors import CORS
from server import app  # make sure your Flask instance is named `app`

from waitress import serve
serve(app, host='0.0.0.0', port=5000)
