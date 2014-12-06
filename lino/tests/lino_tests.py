# -*- coding: utf-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  python manage.py test lino.tests.QuickTest

"""

from django.conf import settings
from lino.utils.djangotest import RemoteAuthTestCase
from lino import dd, rt

# import logging
# logger = logging.getLogger(__file__)
# logger.setLevel("DEBUG")


class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        self.assertEqual(settings.SITE.kernel.__class__.__name__, 'Kernel')
        self.assertEqual(settings.SITE.kernel.site, settings.SITE)
        # self.assertEqual(settings.SITE, dd.site)
        # self.assertEqual(settings.SITE.plugins.lino, dd.apps.lino)
        # this also fails:
        # self.assertEqual(settings.SITE.plugins, dd.apps)


__all__ = ['QuickTest']
