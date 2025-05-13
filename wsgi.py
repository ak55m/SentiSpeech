import sys
import os

# Add the project directory to Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Import the Flask app
from app import app

# This is the application variable that PythonAnywhere will use
application = app 