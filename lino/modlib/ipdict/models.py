# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The models module for this plugin.

"""
from builtins import object

from django.conf import settings

from django.db import models

from lino.api import dd, _

from lino.core.auth import get_auth_middleware


class Connections(dd.VirtualTable):
    """

    """
    label = _("Connections")
    required_roles = dd.login_required(dd.SiteAdmin)
    column_names = "ip_address login_failures blacklisted_since users"
    window_size = (60, 10)


    @classmethod
    def get_data_rows(cls, ar):
        auth = get_auth_middleware()
        for ip, rec in auth.ip_records.items():
            yield rec
    
    @dd.displayfield(_("IP address"))
    def ip_address(self, obj, ar):
        return obj.ip

    @dd.displayfield(_("Blacklisted since"))
    def blacklisted_since(self, obj, ar):
        return obj.blacklisted_since

    @dd.displayfield(_("Login failures"))
    def login_failures(self, obj, ar):
        return obj.login_failures

    @dd.displayfield(_("Users"))
    def users(self, obj, ar):
        return ', '.join([str(x) for x in obj.user_records.values()])

    
            
