#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Temporarily fake the migration to get past the stuck state
python manage.py migrate transactions --fake-initial

# Then force apply all real pending migrations
python manage.py migrate
