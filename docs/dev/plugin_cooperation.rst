==================
Plugin cooperation
==================

- :attr:`lino.core.Plugin.needs_plugins`
- :func:`lino.core.utils.resolve_app`
- :func:`lino.core.inject.inject_field`

- Plugins can register choices to a choicelist of another plugin.  For
  example the :mod:`clocking <lino.modlib.clocking>` plugin adds a
  filter criteria to a table of the :mod:`tickets
  <lino.modlib.tickets>` plugin.

