=======================
Introduction to plugins
=======================

Lino defines two classes :class:`Site <lino.core.site.Site>` and
:class:`Plugin <lino.core.plugin.Plugin>` which are used by Lino
applications to do lots of magic and to make :doc:`apps <application>`
more pleasant to configure.

Application developers usually define a subclass of :class:`Plugin
<lino.core.plugin.Plugin>` in the :xfile:`__init__.py` file of every
app.  For example::

    from lino.api import ad, _
    
    class Plugin(ad.Plugin):
        verbose_name = _("Better calendar")
        extends = 'lino.modlib.cal'
        needs_plugins  = ['lino.modlib.contacts']

This snippet also shows the recommended syntax for importing the
:mod:`lino.api.ad` module.



Configuring plugins
===================

As an application developer you can specify *in your application* that
you want to configure certain plugins by overriding the
:meth:`lino.core.site.Site.setup_plugins` method.

You do this in your application's :xfile:`settings.py`.

For example::

    from lino.projects.std.settings import Site

    class Site(Site):

        def setup_plugins(self):
            super(Site, self).setup_plugins()
            self.plugins.countries.configure(country_code='BE')


As a system administrator you can override these configuration
defaults in your project's :xfile:`settings.py` using the
:func:`configure_plugin <lino.core.site.configure_plugin>` function.

For example, if you want to set the :attr:`country_code
<lino.modlib.countries.Plugin.country_code>` of
:mod:`lino.modlib.countries` to `'DE'`::

    from lino_cosi.projects.apc.settings import *
    configure_plugin('countries', country_code='DE')
    SITE = Site(globals())

Beware the pitfall: :func:`configure_plugin
<lino.core.site.configure_plugin>` must be called *before* the
:setting:`SITE` has been instantiated, otherwise *they will be ignored
silently*.  (It is not easy to prevent accidental calls to *after*
Site initialization because there are scenarios where you want to
instantiate several `Site` objects.)

Uncomplete list of configurable plugin attributes:

- :attr:`lino.modlib.countries.Plugin.country_code` 
- :attr:`lino.modlib.contacts.Plugin.hide_region`

See also :doc:`/admin/settings`.

