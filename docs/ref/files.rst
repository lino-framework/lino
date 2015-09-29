Files
=====

.. xfile:: media/cache/wsdl

  See :blogref:`20120508`.
  
.. xfile:: setup.py

Deserves more documentation.

.. xfile:: models.py

Every Django app usually has a file `models.py`.  See `How to write
reusable apps
<https://docs.djangoproject.com/en/dev/intro/reusable-apps/>`_


.. xfile:: urls.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: manage.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: __init__.py

The Python language requires a file :xfile:`__init__.py` in each
directory that is to be considered as a package.  Read the `Modules
<https://docs.python.org/2/tutorial/modules.html>`_ chapter of the
Python Tutorial for more.

The :xfile:`__init__.py` files of a Django app are often empty, but
with Lino these files can contain :class:`lino.core.plugin.Plugin` class
definitions.

.. xfile:: media

This is the directory where Lino expects certain subdirs.

.. xfile:: config

Lino has a concept of configuration directories that are a bit like 
Django's `templates` directories.
See :mod:`lino.utils.config`.

.. xfile:: .po

:xfile:`.po` files are gettext catalogs. 
They contain chunks of English text as they appear in Lino, 
together with their translation into a given language.
See :doc:`/dev/translate/index`.

.. xfile:: admin_main.html

This is the template used to generate the inner content of the home
page. It is split into two files
:srcref:`admin_main.html<lino/config/admin_main.html>` and
:srcref:`admin_main_base.html<lino/config/admin_main_base.html>`.

.. xfile:: linolib.js
.. xfile:: lino.js

These are obsolete synonyms for :xfile:`linoweb.js`.

