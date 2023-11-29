#!/bin/bash
python -m flake8 --max-line-length=88 .
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
