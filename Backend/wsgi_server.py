from waitress import serve
from server import app  # make sure your Flask instance is named `app`

serve(app, host='0.0.0.0', port=5000)
