Tickets
=======


List of currently **active** tickets:

.. tickets_table:: 
   :filter: e.meta.get('state') in ('open', 'todo')

   *

List of tickets that are **waiting for user feedback**:

.. tickets_table:: 
   :filter: e.meta.get('state') in ('discussion', 'testing')

   *

List of **sleeping** tickets:

.. tickets_table:: 
   :filter: e.meta.get('state') in ('sleeping',)

   *


List of **other** tickets that have a state:

.. tickets_table:: 
   :filter: e.meta.get('state') and not e.meta.get('state') in ('open', 'todo', 'discussion', 'testing', 'sleeping')

   *


List of all tickets:

.. toctree::
   :maxdepth: 1

   all

