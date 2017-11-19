#!/bin/sh

python monit_dashboard.py
python manage.py makemigrations
python manage.py makemigrations configtitania
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

