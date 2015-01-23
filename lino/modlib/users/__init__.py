# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Lino's :mod:`lino.modlib.users` is Lino's replacement for Django's
:mod:`django.contrib.auth` module.  This module does not require
:mod:`django.contrib.sessions` to be installed.  See also
:doc:`/dev/users`. Note that parts of this module are being used by
Lino's core even if it is not among the installed apps.

.. autosummary::
   :toctree:

    models
    utils
    mixins
    choicelists
    fixtures.demo
    fixtures.demo2

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Users")

    def on_init(self):
        super(Plugin, self).on_init()
        self.site.set_user_model('users.User')
