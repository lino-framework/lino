# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.modlib.polls` package provides models and
functionality for managing Polls.

This is the main app for :ref:`polly`.
It is also used in :ref:`welfare`.



.. autosummary::
   :toctree:

    models
    utils
    fixtures.bible
    fixtures.feedback

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Polls")
