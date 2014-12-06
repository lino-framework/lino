# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

- :func:`models_by_base <lino.core.dbutils.models_by_base>`

"""

from django.conf import settings

from lino.core.dbutils import models_by_base

modules = settings.SITE.modules
login = settings.SITE.login
startup = settings.SITE.startup
get_printable_context = settings.SITE.get_printable_context
lookup_filter = settings.SITE.lookup_filter
find_config_file = settings.SITE.confdirs.find_config_file
find_config_files = settings.SITE.confdirs.find_config_files
find_template_config_files = settings.SITE.confdirs.find_template_config_files
makedirs_if_missing = settings.SITE.makedirs_if_missing
relpath = settings.SITE.relpath

def show(*args, **kw):
    return login().show(*args, **kw)


