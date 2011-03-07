@echo off
set DJANGO_SETTINGS_MODULE=lino.sites.std.settings
REM ~ set DJANGO_SETTINGS_MODULE=dsbe.settings
make makedocs html upload
