Minimal applications
====================

The predefined applications that come with Lino are under :mod:`lino.apps`.

They are basically just another module to be added to :setting:`INSTALLED_APPS`,
but one important difference with modules from :mod:`lino.modlib` is that they 
also provide a :xfile:`settings.py` file.

There are two classes of predefined applications:
(a) full-featured and complex applications that are being used on real sites,
and 
(b) the minimal applications used for testing, demonstrations and didactical purposes.

Minimal applications are used for testing, demonstrations and didactical purposes.
They are minimal in the sense that they don't define any applicaton logic 
for themselves, they just use a combination of modules 
from :doc:`/ref/modlib`.  

Currently Lino has the following minimal applications:

- :mod:`min1 <lino.apps.min1>` :
  Uses only the :mod:`contacts <lino.modlib.contacts>` module.
  
- :mod:`min2 <lino.apps.min2>` :
  Uses 
  :mod:`contacts <lino.modlib.contacts>`,
  :mod:`projects <lino.modlib.projects>`,
  :mod:`cal <lino.modlib.cal>`,
  :mod:`outbox <lino.modlib.outbox>`
  and :mod:`uploads <lino.modlib.uploads>`

- :mod:`lino.apps.presto`