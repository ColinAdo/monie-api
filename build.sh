#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations with force if needed
python manage.py migrate --noinput || echo "Migration failed, attempting fake"
python manage.py migrate --fake || echo "Fake migration failed"