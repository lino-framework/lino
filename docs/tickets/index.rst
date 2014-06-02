=======
Tickets
=======


Open for contribution
---------------------

The following tickets are selected for future Lino Core Contributors.
If you understand at least one of them, then you are a potential `Lino
Core Developer <http://saffre-rumma.net/jobs/coredev.html>`_
candidate.

.. tickets_table:: 
   :filter: e.meta.get('state') in ('contrib', )

   *


Active
----------

.. tickets_table:: 
   :filter: e.meta.get('state') in ('open', 'todo')

   *

Waiting
-------

Tickets that are **waiting for feedback** from others.

.. tickets_table:: 
   :filter: e.meta.get('state') in ('discussion', 'testing')

   *

Long-term
----------

.. tickets_table:: 
   :filter: e.meta.get('state') in ('longterm', )

   *

Sleeping
--------

.. tickets_table:: 
   :filter: e.meta.get('state') in ('sleeping',)

   *

Done
--------

.. tickets_table:: 
   :filter: e.meta.get('state') in ('done', 'closed', 'fixed')

   *


Other
-----

.. tickets_table:: 
   :filter: e.meta.get('state') and not e.meta.get('state') in ('open', 'todo', 'discussion', 'testing', 'sleeping', 'longterm', 'contrib', 'done', 'closed', 'fixed')

   *


List of all tickets
-------------------

.. toctree::
   :maxdepth: 1
   :glob:
   
   ?
   ??
   ???
