# -*- coding: utf-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test ui.QuickTest

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings


from django.utils import translation
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError

from lino.utils.djangotest import NoAuthTestCase
from lino.utils.djangotest import RemoteAuthTestCase


class NoAuthTest(NoAuthTestCase):

    def test_anonymous_requests(self):
        """
        Try wether the index page loads.
        """
        if settings.SITE.is_installed('pages'):
            from lino_xl.lib.pages.fixtures import std
            from lino.utils import dpy
            dpy.load_fixture_from_module(std)
            #~ d = load_fixture(std)
            #~ self.assertEqual(d.saved,1)

        #~ with self.settings(DEBUG=True):

        response = self.client.get('')
            #~ response = self.client.get('/',REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='en')
        #~ print response.content
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/foo')
        self.assertEqual(response.status_code, 404)

        response = self.client.head('')
        self.assertEqual(response.status_code, 200)

        response = self.client.options('')
        self.assertEqual(response.status_code, 200)


class RemoteAuthTest(RemoteAuthTestCase):
    maxDiff = None

    def test00(self):
        """
        Initialization.
        """
        if settings.SITE.user_model is None:
            return

        #~ print "20130321 test00 started"
        self.user_root = settings.SITE.user_model(
            username='robin', language='en', profile='900')
        self.user_root.save()

        response = self.client.get(
            '', REMOTE_USER='foo', HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            '', REMOTE_USER='robin', HTTP_ACCEPT_LANGUAGE='en')
        #~ logger.info('20130616 %r',response.content)
        self.assertEqual(response.status_code, 200)
