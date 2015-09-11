.. _howto.settings:

Modifying your local :file:`settings.py`
========================================

This document is for system administrators who want to override
certain settings locally.

To edit your local :xfile:`settings.py` file, go to the project
directory and start your preferred editor on the file `settings.py`::

  cd /usr/local/django/myproject
  nano settings.py

:envvar:`DJANGO_SETTINGS_MODULE`

After modifying your :xfile:`settings.py` you must restart all Lino
services (i.e. Apache and possibly some other site-specific services).

The :xfile:`settings.py` file must be valid Python syntax.  One
pitfall if you have no experience with Python is that *indentation* is
important.  There must be *four spaces* in front of every class
attribute.

In case of doubt, before restarting the server, you may issue the
following command to test whether your :xfile:`settings.py` is okay::

  python manage.py validate

See also :doc:`/dev/settings` and :doc:`/dev/plugins`.

