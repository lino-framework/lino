Jargon
=============



.. _pk:

primary key
-----------

The **primary key** of a database table (which we call "Model" in
Lino) is one of it fields which holds the unique identification of
each row.  This field is often not shown to the user.

.. _gfk:

GenericForeignKey
-----------------

See `Django docs
<https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericForeignKey>`_

.. _ise:

Internal Server Error
---------------------

When an exception occurs that is not catched, then Lino behaves like 
any Django application and return a HTTP return code 500.


.. _admin:

System administrator
--------------------

A system administrator is a person who installs an existing Lino application.
He or she doesn't need to write Python code except for the :xfile:`settings.py` 
file.

.. _dev:

Lino application developer
--------------------------

A Lino application developer is a Python programmer who uses Lino while 
writing his own application.

