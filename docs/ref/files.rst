Files
=====

.. xfile:: media/cache/wsdl

  See :doc:`/blog/2012/0508`.
  
.. xfile:: setup.py

  Deserves more documentation.

.. xfile:: settings.py

See :doc:`/tutorials/polls` 

.. xfile:: urls.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: manage.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: __init__.py

The Python language requires a file :xfile:`__init__.py` 
in each directory that is to be considered as a package.
:xfile:`__init__.py` are often empty (but not always).

.. xfile:: media

See 

.. xfile:: config

Lino has a concept of configuration directories that are a bit like 
Django's `templates` directories.
See :mod:`lino.utils.config`.

.. xfile:: linolib.js
.. xfile:: lino.js

The ExtJS3 user interface generates a series of files 
:file:`lino_PROFILE_LANG.js` 
at server startup which contain the 
client side application logic. 
The first part of this file comes from
a file :srcref:`/lino/ui/extjs3/linolib.js`,
the second part is purely generated from your models and reports).


.. xfile:: .po

:xfile:`.po` files are gettext catalogs. 
They contain chunks of English text as they appear in Lino, 
together with their translation into a given language.
See :doc:`/admin/translate`.

