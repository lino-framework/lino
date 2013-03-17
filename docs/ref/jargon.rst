Jargon
=============


.. _lf:

lino-framework.org
------------------

`lino-framework.org` is currently Lino's primary domain. 
It is hosted in collaboration with 
`Active Systems OÜ <http://active.ee>`.

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
    
