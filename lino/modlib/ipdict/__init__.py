# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from datetime import timedelta
from lino.utils import get_client_ip_address
from lino.api import ad

class IPRecord(object):
    def __init__(self, addr):
        self.addr = addr
        self.login_failures = 0
        self.blacklisted_since = None
        # self.last_login = None
        # self.last_failure = None
        # self.last_request = None

    def __repr__(self):  # just for debugging
        return "{} {} {}".format(
            self.addr, self.login_failures, self.blacklisted_since)


class Plugin(ad.Plugin):

    max_blacklist_time = timedelta(minutes=1)
    max_failed_auth_per_ip = 4 # Should be set in settings.SITE?
    ip_records = {}

    def get_ip_record(self, request):
        addr = get_client_ip_address(request)
        rec = self.ip_records.get(addr, None)
        if rec is None:
            rec = IPRecord(addr)
            self.ip_records[addr] = rec
        return rec

    def pop_ip_record(self, request):
        addr = get_client_ip_address(request)
        return self.ip_records.pop(addr, None)
