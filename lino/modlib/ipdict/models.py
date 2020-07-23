# -*- coding: UTF-8 -*-
# Copyright 2017-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from datetime import datetime
from django.conf import settings

# from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.contrib.auth.signals import user_logged_in, user_login_failed
# from django.contrib.auth.signals user_logged_out
from lino.api import dd, _


def format_timestamp(dt):
    if dt is None:
        return ''
    return u"{} {} ({})".format(
        dt.strftime(settings.SITE.date_format_strftime),
        dt.strftime(settings.SITE.time_format_strftime),
        naturaltime(dt))


class Connections(dd.VirtualTable):
    """

    """
    label = _("Connections")
    required_roles = dd.login_required(dd.SiteAdmin)
    column_names = "last_request:30 ip_address:12 login_failures:5 blacklisted_since:12 username:20 last_login:30"
    window_size = (90, 12)


    @classmethod
    def get_data_rows(cls, ar):
        # return dd.plugins.ipdict.ip_records.values()
        never = settings.SITE.startup_time
        return reversed(sorted(
            dd.plugins.ipdict.ip_records.values(),
            key=lambda x: x.last_request or never))

    @dd.displayfield(_("IP address"))
    def ip_address(self, obj, ar):
        return obj.addr

    @dd.displayfield(_("Blacklisted since"))
    def blacklisted_since(self, obj, ar):
        return format_timestamp(obj.blacklisted_since)

    @dd.displayfield(_("Login failures"))
    def login_failures(self, obj, ar):
        return obj.login_failures

    @dd.displayfield(_("Username"))
    def username(self, obj, ar):
        return  obj.username

    @dd.displayfield(_("Last request"))
    def last_request(self, obj, ar):
        return format_timestamp(obj.last_request)

    @dd.displayfield(_("Last login"))
    def last_login(self, obj, ar):
        return format_timestamp(obj.last_login)




@dd.receiver(user_login_failed)
def on_login_failed(sender=None, credentials=None, request=None,
                    **kwargs):
    ipdict = settings.SITE.plugins.ipdict
    rec = ipdict.get_ip_record(request, 'anonymous')
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


@dd.receiver(user_logged_in)
def on_logged_in(sender=None, request=None, user=None, **kwargs):
    # when an IP was blacklisted, got unlocked after
    # max_blacklist_time and then received a successful login,
    # then all sins of anonymous are being erased:
    ipdict = settings.SITE.plugins.ipdict
    rec = ipdict.get_ip_record(request, 'anonymous')
    rec.blacklisted_since = None
    rec.login_failures = 0

    # record the login time for username
    rec = ipdict.get_ip_record(request, user.username)
    rec.last_login = datetime.now()
