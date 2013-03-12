Fixtures
========

>>> from tutorials.auto_create.models import *

Create a demo database:

>>> call_command('initdb_demo',interactive=False)
Creating tables ...
Creating table ui_siteconfig
Creating table auto_create_tag
Installing custom SQL ...
Installing indexes ...

>>> print Foo

Voilà