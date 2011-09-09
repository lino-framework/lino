Files
=====

.. xfile:: .dtl

Configuration file that describes the layout of (one tab of) 
a :term:`Detail Window`.
See :doc:`/topics/dtl`.

.. xfile:: settings.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: urls.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: manage.py

See http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project

.. xfile:: media

See 

.. xfile:: config

Lino has a concept of configuration directories that are a bit like 
Django's `templates` directories.
See :mod:`lino.utils.config`.

.. xfile:: linolib.js
.. xfile:: lino.js

The ExtJS3 user interface generates a big file :file:`lino.js` at server startup which 
contains the client side application logic. 
The first part of this file comes from
a file :srcref:`/lino/ui/extjs3/linolib.js` 
(the second part is purely generated from your models and reports).


.. xfile:: .po

:xfile:`.po` files are gettext catalogs. 
They contain chunks of English text as they appear in Lino, 
together with their translation into a given language.
See :doc:`/admin/translate`.

