Jargon
=============


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

.. _lf:

lino-framework.org
------------------

`lino-framework.org` is currently Lino's primary domain. 
It is hosted in collaboration with 
`Active Systems OÜ <http://active.ee>`_.

.. _ddt:

Double Dump Test
----------------

A `Double Dump Test` is a method to test 
for possible database problems e.g. after 
a :ref:`datamig`: 
a first dump writes a picture of the database to a Python 
fixture `a.py`, then we use `manage.py initdb a` to load that picture 
to the database, then perform a second dump to a fixture `b.py`. 
And then we launch `diff a.py b.py` to veryfy that both pictures are identical.
    

.. _patrols: 

Lino Patrols
------------

See http://patrols.lino-framework.org




