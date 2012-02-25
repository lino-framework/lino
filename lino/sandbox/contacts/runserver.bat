@echo off
REM ~ set REMOTE_USER=user
REM ~ set REMOTE_USER=root
set REMOTE_USER=alice
REM ~ if exist w:\*.* subst w: /d
REM ~ subst w: media\webdav 
start python manage.py runserver 
