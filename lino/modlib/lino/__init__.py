# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
.. autosummary::
   :toctree:

   models
   management.commands
   tests

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    ui_label = _("Lino")

    # url_prefix = 'lino'

    media_name = 'lino'
