# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module deserves a better docstring.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings


class Handle:

    def __init__(self):
        self.ui = settings.SITE.ui

    def setup(self, ar):
        self.ui.setup_handle(self, ar)
        #~ settings.SITE.ui.setup_handle(self,ar)


