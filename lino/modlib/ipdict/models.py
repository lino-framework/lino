# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from datetime import datetime
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.auth.signals import user_logged_out
from lino.api import dd

@dd.receiver(user_login_failed)
def on_login_failed(sender=None, credentials=None, request=None,
                    **kwargs):
    rec = settings.SITE.plugins.ipdict.get_ip_record(request, 'anonymous')
    # user failed to authenticate
    rec.login_failures += 1
    if rec.login_failures >= ipdict.max_failed_auth_per_ip:
        # maybe a robot is trying to log in with brute force
        # and waited patiently for max_blacklist_time to pass,
        # and now continues to try. In that case we don't
        # forget the blacklisted_since, so the robot must now
        # wait a full minute for every attempt
        if rec.blacklisted_since is None:
            rec.blacklisted_since = datetime.now()


@dd.receiver(user_logged_out)
def on_logged_out(sender=None, request=None, user=None, **kwargs):
    settings.SITE.plugins.ipdict.pop_ip_record(request, user.username)

@dd.receiver(user_logged_in)
def on_logged_in(sender=None, request=None, user=None, **kwargs):
    # when an IP was blacklisted, got unlocked after
    # max_blacklist_time and then received a successful login,
    # then all sins of anonymous are being erased:
    settings.SITE.plugins.ipdict.pop_ip_record(request, 'anonymous')
    # rec = ipdict.get_ip_record(request, 'anonymous')
    # rec.blacklisted_since = None
    # rec.login_failures = 0
    #
    # # record the login time for username
    # rec = ipdict.get_ip_record(request, user.username)
    # rec.last_login = datetime.now()
