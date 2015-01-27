=======================
Introduction to plugins
=======================

Lino defines two classes :class:`Site <lino.core.site.Site>` and
:class:`Plugin <lino.core.plugin.Plugin>` which are heavily used to do
lots of magic and to make apps more pleasant to configure.

Example::

    from lino.api import ad
    
    class Plugin(ad.Plugin):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']

