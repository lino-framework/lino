# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The default URLconf module, defines the variable `urlpatterns` 
as required by Django.
Application code doesn't need to worry about this.

This is found by Django because 
:mod:`lino.projects.std.settings`
:setting:`ROOT_URLCONF` 
is set to ``'lino.ui.urls'``.

"""

from django.conf import settings
settings.SITE.startup()
urlpatterns = settings.SITE.ui.get_patterns()
