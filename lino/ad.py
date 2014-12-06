# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Example::

    from lino import ad
    
    class Plugin(ad.Plugin):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']
    
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from lino.utils.xmlgen.html import E
# from lino.utils.mldbc import to_locale, LanguageInfo


from lino.core.plugin import Plugin
from lino.core.site_def import Site, TestSite, configure_plugin


__all__ = ['Site', 'TestSite', 'Plugin', 'configure_plugin', '_']
