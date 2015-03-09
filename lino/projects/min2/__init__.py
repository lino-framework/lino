"""A minimal application used by a number of tests and tutorials. It
is not meant to be actually useful in the real world.

It is a little bit less minimal than :mod:`lino.projects.min1` in that
it adds some more modlib plugins:

- :mod:`lino.modlib.changes`
- :mod:`lino.modlib.excerpts`
- :mod:`lino.modlib.addresses`
- :mod:`lino.modlib.reception`
- :mod:`lino.modlib.iban`
- :mod:`lino.modlib.sepa`
- :mod:`lino.modlib.notes`
- :mod:`lino.modlib.projects`
- :mod:`lino.modlib.humanlinks`
- :mod:`lino.modlib.households`
- :mod:`lino.modlib.pages`

It overrides the :mod:`lino.modlib.contacts` plugin by its own version
``lino.projects.min2.modlib.contacts``.


"""
