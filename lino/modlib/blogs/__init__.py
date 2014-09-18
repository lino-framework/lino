# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    verbose_name = _("Blog")


