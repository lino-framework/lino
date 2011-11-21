South cheat sheet
=================

- schemamigration : create a new migration
- migrate : apply migrations


======================================== =================================================
manage.py schemamigration APP --initial  create a first migration
manage.py schemamigration APP --auto     create a migration with changes since last migration
manage.py migrate APP                    apply all necessary migrations
manage.py migrate --list                 show list of previously applied migrations
======================================== =================================================
