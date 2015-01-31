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

As an :doc:`/team/lad` you can specify *in your application* that
you want to configure certain plugins by overriding the 
:meth:`lino.core.site.Site.setup_plugins` method. 

You do this in your application's :xfile:`settings.py`.

For example::

    from lino.projects.std.settings import Site

    class Site(Site):

        def setup_plugins(self):
            super(Site, self).setup_plugins()
            self.plugins.countries.configure(country_code='BE')


As a :doc:`/team/sysadm` your can override these configuration
defaults using the :meth:`configure_plugin
<lino.core.site.Site.configure_plugin>` method. For example::

    from lino_cosi.projects.apc.settings import *
    configure_plugin('countries', country_code='BE')
    SITE = Site(globals())
