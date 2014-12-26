# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.ad` module is a shortcut to those parts of Lino which
are used in your :xfile:`settings.py` files and in the
:xfile:`__init__.py` files of your apps.  The name ``ad`` stands for
"Application Design".  Application design happens **during** the
import of your Django **settings** and **before** your **models** get
imported.

Lino defines two classes :class:`Site <lino.core.site_def.Site>` and
:class:`Plugin <lino.core.plugin.Plugin>` which are heavily used to do
lots of magic and to make apps more pleasant to configure.


Example::

    from lino import ad
    
    class Plugin(ad.Plugin):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']

.. autosummary::

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from lino.utils.xmlgen.html import E
# from lino.utils.mldbc import to_locale, LanguageInfo


from lino.core.plugin import Plugin
from lino.core.site_def import Site, TestSite, configure_plugin


__all__ = ['Site', 'TestSite', 'Plugin', 'configure_plugin', '_']
