@echo off
python manage.py syncdb --noinput 
python manage.py loaddata demo
