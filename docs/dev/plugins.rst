=======================
Introduction to plugins
=======================

Lino defines two classes :class:`Site <lino.core.site.Site>` and
:class:`Plugin <lino.core.plugin.Plugin>` which are heavily used to do
lots of magic and to make apps more pleasant to configure.


The Plugin class is defined in the :xfile:`__init__.py` file of every
app.
For example::

    from lino.api import ad
    
    class Plugin(ad.Plugin):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']



Configuring plugins
===================

As an application developer you can specify *in your application* that
you want to configure certain plugins by overriding the 
:meth:`lino.core.site.Site.setup_plugins` method. For example::

    class Site(Site):

        def setup_plugins(self):
            super(Site, self).setup_plugins()
            self.plugins.countries.configure(country_code='BE')


As a local system administrator your can override these configuration
defaults using the :meth:`configure_plugin
<lino.core.site.Site.configure_plugin>` method. For example::

    from foo.bar.settings import *
    configure_plugin('countries', country_code = 'BE')
    SITE = Site(globals())
