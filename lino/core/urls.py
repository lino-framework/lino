# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The default URLconf module, defines the variable `urlpatterns` as
required by Django.  Lino application code doesn't need to worry about
this.

This is found by Django because :mod:`lino.projects.std.settings`
:setting:`ROOT_URLCONF` is set to ``'lino.core.urls'``.

"""

from django.conf import settings

# from lino.core.signals import database_ready

# settings.SITE.startup()
# database_ready.send(settings.SITE)

# from lino.modlib.extjs.urls import urlpatterns

urlpatterns = settings.SITE.ui.get_patterns()
