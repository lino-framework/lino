# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Lino's :mod:`lino.modlib.users` is Lino's replacement for Django's
:mod:`django.contrib.auth` module. See also :doc:`/dev/users`.

.. autosummary::
   :toctree:

    models
    utils
    mixins
    choicelists
    fixtures.demo
    fixtures.demo2


This module does not require :mod:`django.contrib .sessions` to be
installed. See :srcref:`docs/tickets/31` for discussion.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Users")

    def on_init(self):
        super(Plugin, self).on_init()
        self.site.set_user_model('users.User')
