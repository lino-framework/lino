Settings inheritance
====================

The central place for a Django site is the :xfile:`settings.py` file.

Lino extends this idea with the :class:`lino.Lino` class. 

On a Lino site ou must define a Lino-specific variable
``LINO`` which must hold an instance of 
:class:`lino.Lino` (or some subclass thereof).
Note that the :mod:`lino` module may be imported from a 
Django settings file because 
it does not import any Django modules.

:djangoticket:`14297` 