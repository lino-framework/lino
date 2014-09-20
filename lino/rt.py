# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings

modules = settings.SITE.modules
login = settings.SITE.login
startup = settings.SITE.startup


def show(*args, **kw):
    return login().show(*args, **kw)

from django.utils import translation
get_language = translation.get_language

