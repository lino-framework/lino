# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The models module for this plugin.

.. autosummary::
   :toctree:

    models
    middleware

"""

from datetime import timedelta
from lino.utils import get_client_ip_address
from lino.api import ad

class IPRecord(object):
    def __init__(self, addr, username):
        self.addr = addr
        self.username = username
        self.login_failures = 0
        self.blacklisted_since = None
        self.last_login = None
        self.last_failure = None
        self.last_request = None

# class UserIPRecord(object):
#     def __init__(self, ip, username):
#         self.ip = ip

#     # def __str__(self):
#     #     s = u"{username} {last_request} ({ago})".format(
#     #         username=self.username,
#     #         last_request=format_timestamp(self.last_request),
#     #         ago=naturaltime(self.last_request)
#     #     )
#     #     # idletime = datetime.now() - self.last_request
#     #     # if idletime > max_idletime:
#     #     #     s += _(" ({})").format(naturaltime(self.last_request))
#     #     return s


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    max_blacklist_time = timedelta(minutes=1)
    max_failed_auth_per_ip = 4 # Should be set in settings.SITE?
    # blacklist = {}
    ip_records = {}

    def get_ip_record(self, request, username):
        addr = get_client_ip_address(request)
        k = (addr, username)

        ip = self.ip_records.get(k, None)
        if ip is None:
            ip = IPRecord(addr, username)
            self.ip_records[k] = ip
        return ip

    def pop_ip_record(self, request, username):
        addr = get_client_ip_address(request)
        k = (addr, username)
        return self.ip_records.pop(k, None)
