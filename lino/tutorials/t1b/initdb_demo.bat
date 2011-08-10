@echo off
python manage.py initdb std few_countries few_cities few_languages props demo --traceback --noinput %*

