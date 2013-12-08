=======================================
Patterns for communication between apps
=======================================


.. _app_inheritance:

App inheritance
===============


The :mod:`lino.ad` module

The :class:`djangosite..App` class

One problem with app inheritance are the fixtures and the 
management commands.

For `fixtures` I currently use the workaround of creating 
one module for every fixture of the parent, and importing 
`objects` from the parent fixture. 
For example 
the `lino_faggio/cal/fixtures`directory  -> lino/apps/cal/fixtures


Django discovers management commands by checking whether the app
module has a submodule "management" and then calling
:meth:`os.listdir` on that module's "commands" subdirectory.  (See
Django's `core/management/__init__.py` file)

I'll make a first attempt using symbolic links::

  lino_faggio/cal/fixtures -> lino/apps/cal/fixtures
  lino_faggio/apps/management -> lino/apps/cal/management

