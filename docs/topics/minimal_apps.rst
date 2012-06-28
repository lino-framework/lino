Minimal applications
====================

Minimal applications are used for testing, demonstrations and didactical purposes.

They are minimal in the sense that they don't define any applicaton logic 
for themselves, they just use a combination of modules 
from :doc:`/ref/modlib`.  

Currently Lino has the following minimal applications:

- :mod:`min1 <lino.apps.min1>` :
  Uses only the :mod:`contacts <lino.modlib.contacts>` module.
  
- :mod:`min2 <lino.apps.min2>`  
  :mod:`contacts <lino.modlib.contacts>`
  :mod:`contacts <lino.modlib.projects>`
  :mod:`cal <lino.modlib.cal>`
  :mod:`outbox <lino.modlib.outbox>`
  :mod:`outbox <lino.modlib.uploads>`

- :mod:`lino.apps.min2`  :mod:`lino.modlib.contacts`
- :mod:`lino.apps.presto`