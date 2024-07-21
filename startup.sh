#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
gunicorn --bind 0.0.0.0 --workers 2 app:app