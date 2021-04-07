# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging ; logger = logging.getLogger('unittest')


import sys
import argparse
import unittest
import time

from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta
from django.conf import settings

from lino.api import dd
from lino.utils.test import DemoTestCase


class TestCase(DemoTestCase):

    tested_urls = ('/', '/?su=3', '/?su=1234')

    def test_get(self):

        if False:
            # switched off because it causes a message "Not found: /foo"
            res = self.client.get("/foo")
            self.assertEqual(
                res.status_code, 404,
                "Status code {} other than 404".format(res.status_code))

        for url in self.tested_urls:
            # print("20200513", url)
            res = self.client.get(url)
            self.assertEqual(
                res.status_code, 200,
                "Status code %s other than 200 for anonymous on GET %s" % (
                    res.status_code, url))

        if settings.SITE.user_model:
            for user in settings.SITE.user_model.objects.all():
                if user.user_type:
                    d = self.login(user.username, '1234')
                    # self.client.force_login(user)
                    for url in self.tested_urls:
                        # logger.debug("%s gets %s", user.username, url)
                        print("{} gets {}".format(user.username, url))
                        res = self.client.get(url)
                        self.assertEqual(
                            res.status_code, 200,
                            "Status code {} for {} on GET {}".format(
                                res.status_code, user, url))

    def test_ipdict(self):
        if not settings.SITE.use_ipdict:
            return
        ipdict = dd.plugins.ipdict

        self.assertEqual(ipdict.max_failed_auth_per_ip, 4)
        self.assertEqual(ipdict.max_blacklist_time, timedelta(minutes=1))

        # For this test we reduce max_blacklist_time because we are going to
        # simulate a hacker who patiently waits:
        ipdict.max_blacklist_time = timedelta(seconds=1)

        self.assertEqual(ipdict.ip_records, {})

        def login(pwd):
            d = self.login('robin', pwd)
            return d.message

        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        rec = ipdict.ip_records['127.0.0.1']
        self.assertEqual(rec.login_failures, 1)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 2)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 3)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 4)
        self.assertEqual(login("bad"), 'Too many authentication failures from 127.0.0.1')

        # login_failures doesn't continue to increase when the ip is blacklisted:
        self.assertEqual(rec.login_failures, 4)

        # Even with the right password you cannot unlock a blacklisted ip
        self.assertEqual(login("1234"), 'Too many authentication failures from 127.0.0.1')

        # After max_blacklist_time, the IP gets removed from the blacklist, but
        # every new failure will now blacklist it again, the
        # max_failed_auth_per_ip no longer counts.

        time.sleep(1)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 5)
        self.assertEqual(login("bad"), 'Too many authentication failures from 127.0.0.1')
        self.assertEqual(rec.login_failures, 5)

        time.sleep(1)
        self.assertEqual(login("1234"), 'Now logged in as Robin Rood')

        # Once you manage to authenticate, your ip address gets removed from the
        # blacklist, i.e. when you log out and in for some reason, you get again
        # max_failed_auth_per_ip attempts

        self.assertEqual(ipdict.ip_records, {})
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        rec = ipdict.ip_records['127.0.0.1']
        self.assertEqual(rec.login_failures, 1)


class Command(BaseCommand):

    help = "Run a series of standard read-only tests in this project."

    # requires_system_checks = False

    def run_from_argv(self, argv):
        sys.argv = sys.argv[1:]
        unittest.main(self.__module__)

    # def handle(self, *args, **options):
    #     sys.argv = sys.argv[1:]
    #     unittest.main(self.__module__)
