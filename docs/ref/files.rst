Files
=====

.. xfile:: .dtl

Configuration file that describes the layout of (one tab of) a :term:`Detail Window`.

.. xfile:: settings.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: urls.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: manage.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: lino_settings.py

Loaded during :meth:`lino.lino_site.LinoSite.setup`.

Located usually in your :setting:`PROJET_DIR` (the same directory as :xfile:`settings.py`), 
except if you change the default value of :setting:`LINO_SETTINGS`.


.. xfile:: linolib.js

See :srcref:`/lino/ui/extjs3/linolib.js`

.. xfile:: initdb.py

A script that does a syncdb and reset of the database, and loads specified fixtures
