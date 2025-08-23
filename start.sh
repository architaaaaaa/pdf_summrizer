#!/bin/bash
# A simple start script for Render

# Use gunicorn to run the application.
# The format is 'module_name:app_variable_name'
# 'app' is the name of your app.py file (without the .py)
# 'app' is also the name of the Flask app instance (app = Flask(__name__))
gunicorn --bind 0.0.0.0:$PORT app:app
