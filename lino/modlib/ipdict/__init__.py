# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The models module for this plugin.

.. autosummary::
   :toctree:

    models
    middleware

"""

from lino.api import ad
from datetime import timedelta

class IPRecord(object):
    def __init__(self, addr, username):
        self.addr = addr
        self.username = username
        self.login_failures = 0
        self.blacklisted_since = None
        self.last_login = None
        self.last_failure = None
        self.last_request = None

# #six.python_2_unicode_compatible
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
        addr = self.get_client_id(request)
        k = (addr, username)
        
        ip = self.ip_records.get(k, None)
        if ip is None:
            ip = IPRecord(addr, username)
            self.ip_records[k] = ip
        return ip
    
    @staticmethod
    def get_client_id(request):
        # from http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip or "(unknown)"  # see ticket #2605


    def setup_site_menu(config, site, user_type, m):
        m.add_action(site.modules.ipdict.Connections)
