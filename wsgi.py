"""
WSGI entry point for DigitalOcean deployment
"""
import sys
import os

# Add webapp directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'webapp'))

from webapp.app import app

if __name__ == "__main__":
    app.run()
