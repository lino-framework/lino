Modifying your local `settings.py`
==================================

This document is for system administrators who want to override
certain settings locally.

To edit your local :xfile:`settings.py` file, go to the project
directory and start your preferred editor on the file `settings.py`::

  cd /usr/local/django/dsbe_eupen
  nano settings.py

After modifying your settings.py you must restart all Lino services
(i.e. Apache and possibly some other site-specific services).

Note that the `settings.py` file must be valid Python syntax. One
pitfall if you have no experience with Python is that *indentation* is
important. There must be *four spaces* in front of every class attribute.

In case of doubt, before restarting the server, you may issue the
following command to test whether your :xfile:`settings.py` is okay::

  python manage.py validate


TODO: continue explanations.

- :doc:`/dev/ad`
- djangosite/docs/usage

