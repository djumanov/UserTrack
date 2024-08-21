#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

# Start the Django development server
echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000
