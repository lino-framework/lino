Modifying your local `settings.py`
==================================

To edit your local :xfile:`settings.py` 
file, go to the project directory and start
your preferred editor on the file `settings.py`::

  cd /usr/local/django/dsbe_eupen
  nano settings.py

After modifying your settings.py you must restart 
all Lino services (i.e. Apache and possibly some 
other site-specific services).

Either step by step::

  ./stop
  ./start

Or both at once::

  ./restart

The central reference documentation for all Lino settings is here:

http://lino.saffre-rumma.net/autodoc/lino.html

For example you want to modify the encoding of .csv files generated
by Lino to "latin". The `csv_params` parameter is documented here:

http://lino.saffre-rumma.net/autodoc/lino.html#lino.Lino.csv_params

Edit your settings.py and change the following::

  class Lino(Lino):
      ...
      csv_params = dict(delimiter=';')
      ...

into::

  class Lino(Lino):
      ...
      csv_params = dict(delimiter=';',encoding='latin')
      ...

Note that the `settings.py` file must be valid Python syntax. One
pitfall if you have no experience with Python is that *indentation* is
important. There must be *four spaces* in front of every class attribute.

In case of doubt, before restarting the server, you may issue the
following command to test whether your settings.py is okay::

  python manage.py validate