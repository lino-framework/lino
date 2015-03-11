.. _dev.vtables: 

==============
Virtual tables
==============

.. include:: /include/wip.rst

Here is the :xfile:`models.py` file we will use for this tutorial:

.. literalinclude:: models.py
  
Some setup for doctest:
  
>>> from __future__ import print_function
>>> from lino.api import rt
>>> from lino.api.shell import *
>>> globals().update(vtables.__dict__)


>>> rt.show(CitiesAndInhabitants)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
========= ========= ============
 Country   City      Population
--------- --------- ------------
 Belgium   Eupen     17000
 Belgium   Liege     400000
 Belgium   Raeren    5000
 Estonia   Tallinn   400000
 Estonia   Vigala    1500
========= ========= ============
<BLANKLINE>

