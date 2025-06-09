#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Only apply migrations (don't generate new ones)
python manage.py migrate