#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Create migrations for all apps
mkdir -p auths/migrations/
mkdir -p transactions/migrations/
touch auths/migrations/__init__.py
touch transactions/migrations/__init__.py

# Generate migrations for all apps
python manage.py makemigrations auths || echo "Could not make auths migrations"
python manage.py makemigrations transactions || echo "Could not make transactions migrations"

# Apply all migrations
python manage.py migrate