#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Make sure migrations folder exists
mkdir -p transactions/migrations/

# Force create initial migration if missing
python manage.py makemigrations transactions --noinput || true

# Apply migrations
python manage.py migrate