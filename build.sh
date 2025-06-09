#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations

# Then force apply all real pending migrations
python manage.py migrate auths transactions 
