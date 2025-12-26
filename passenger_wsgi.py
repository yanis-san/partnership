"""
Passenger WSGI entry point for cPanel deployment.
This file is required by Passenger to serve the Django application.
"""

import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the WSGI application from Django config
from config.wsgi import application
