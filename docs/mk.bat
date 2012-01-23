@echo off
set DJANGO_SETTINGS_MODULE=lino.apps.std.settings
REM ~ set DJANGO_SETTINGS_MODULE=lino.apps.sphinxdocs.settings
REM ~ set DJANGO_SETTINGS_MODULE=dsbe.settings
make html upload
