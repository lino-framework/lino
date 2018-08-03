# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.conf import settings

from lino.core.utils import models_by_base

models = settings.SITE.models
"""
"""

from lino.core.exceptions import ChangedAPI
actors = modules = ChangedAPI(
    "Replace rt.modules and rt.actors by rt.models")

# actors = settings.SITE.models

login = settings.SITE.login
startup = settings.SITE.startup
# get_printable_context = settings.SITE.get_printable_context
lookup_filter = settings.SITE.lookup_filter
find_config_file = settings.SITE.confdirs.find_config_file
find_config_files = settings.SITE.confdirs.find_config_files
find_template_config_files = settings.SITE.confdirs.find_template_config_files
makedirs_if_missing = settings.SITE.makedirs_if_missing
# relpath = settings.SITE.relpath
# get_settings_subdirs = settings.SITE.get_settings_subdirs
# is_local_project_dir = settings.SITE.is_local_project_dir


def get_template(*args, **kw):
    return settings.SITE.plugins.jinja.renderer.jinja_env.get_template(
        *args, **kw)


def show(*args, **kw):
    return login().show(*args, **kw)


def send_email(*args, **kw):
    "Shortcut to :meth:`lino.core.site.Site.send_email`."
    return settings.SITE.send_email(*args, **kw)


def html_text(*args, **kw):
    return settings.SITE.kernel.default_renderer.html_text(
        *args, **kw)
