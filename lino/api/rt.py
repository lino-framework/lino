# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module is a shortcut to miscellaneous functions and classes which
are available "at runtime", i.e. when the Django machine has been
initialized.

You may *import* it at the global namespace of a :xfile:`models.py`
file, but you can *use* most of it only when the :func:`startup`
function has been called.

.. attribute:: plugins

    Shortcut to :attr:`lino.core.site.Site.plugins`

.. attribute:: models

    Shortcut to :attr:`lino.core.site.Site.models`

"""

from django.conf import settings

from lino.core.utils import models_by_base

models = settings.SITE.modules
modules = settings.SITE.modules  # deprecated

login = settings.SITE.login
startup = settings.SITE.startup
# get_printable_context = settings.SITE.get_printable_context
lookup_filter = settings.SITE.lookup_filter
find_config_file = settings.SITE.confdirs.find_config_file
find_config_files = settings.SITE.confdirs.find_config_files
find_template_config_files = settings.SITE.confdirs.find_template_config_files
makedirs_if_missing = settings.SITE.makedirs_if_missing
relpath = settings.SITE.relpath
# get_settings_subdirs = settings.SITE.get_settings_subdirs
# is_local_project_dir = settings.SITE.is_local_project_dir


def get_template(*args, **kw):
    """Shortcut to :meth:`get_template` on the global `jinja2.Environment`
    (:attr:`jinja_env <lino.core.site.Site.jinja_env>`, see
    :mod:`lino.core.web`).

    """
    return settings.SITE.plugins.jinja.renderer.jinja_env.get_template(
        *args, **kw)


def show(*args, **kw):
    """Calls :meth:`show <lino.core.requests.BaseRequest.show>` on a
    temporary anonymous session (created using
    :meth:`rt.login <lino.core.site.Site.login>`).

    """
    return login().show(*args, **kw)


def emit_system_note(*args, **kw):
    "Shortcut to :meth:`lino.core.site.Site.emit_system_note`."
    return settings.SITE.emit_system_note(*args, **kw)


def send_email(*args, **kw):
    "Shortcut to :meth:`lino.core.site.Site.send_email`."
    return settings.SITE.send_email(*args, **kw)
