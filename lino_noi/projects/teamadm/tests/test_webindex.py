# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils.djangotest import WebIndexTestCase

from lino.utils.djangotest import RemoteAuthTestCase


class TestCase(RemoteAuthTestCase):

    def test(self):

        self.assertEqual(1+1, 2)
