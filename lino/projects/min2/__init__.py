"""A minimal application used by a number of tests and tutorials. It
is not meant to be actually useful in the real world.

It is a little bit less minimal than :mod:`lino.projects.min1` in that
it adds some more modlib plugins:

- :mod:`lino.modlib.changes`
- :mod:`lino.modlib.excerpts`
- :mod:`lino.modlib.addresses`
- :mod:`lino.modlib.reception`
- :mod:`lino.modlib.sepa`
- :mod:`lino.modlib.notes`
- :mod:`lino.modlib.projects`
- :mod:`lino.modlib.humanlinks`
- :mod:`lino.modlib.households`
- :mod:`lino.modlib.pages`

This is also a **usage example** of :doc:`/dev/plugin_inheritance`
because if overrides the :mod:`lino.modlib.contacts` plugin by its own
version ``lino.projects.min2.modlib.contacts`` (which is not included
in this documentation tree for technical reasons, and anyway you
should inspect the source code if you want to go futher).

The package has a **test suite** for testing some of the plugins it
uses:

.. autosummary::
   :toctree:

   tests.test_addresses
   tests.test_birth_date
   tests.test_min2
   tests.test_cal


"""
