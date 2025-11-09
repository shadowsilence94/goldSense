"""
Main application entry point for DigitalOcean
Imports the Flask app from webapp
"""
import os
import sys

# Ensure webapp is in path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from webapp.app import app

# This is what gunicorn will look for
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
