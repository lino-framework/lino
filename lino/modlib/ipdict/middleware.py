# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre.
# License: BSD, see LICENSE for more details.

from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from lino.core.auth import NOT_NEEDED, SessionUserMiddleware

class IPRecord(object):
    def __init__(self, ip):
        self.ip = ip
        self.login_failures = 0
        self.blacklisted_since = None
        self.user_records = {}
        
    def get_user_record(self, username):
        ur = self.user_records.get(username, None)
        if ur is None:
            ur = UserIPRecord(self.ip, username)
            self.user_records[username] = ur
        return ur
    
    def record_login(self, username):
        ur = self.get_user_record(username)
        ur.last_login = datetime.now()
        
    def record_request(self, username):
        ur = self.get_user_record(username)
        ur.last_request = datetime.now()
        

class UserIPRecord(object):
    def __init__(self, ip, username):
        self.ip = ip
        self.username = username
        self.last_login = None
        self.last_failure = None
        self.last_request = None

    def __str__(self):
        return "{username} ({last_request})".format(
            username=self.username, last_request=self.last_request)
    
class Middleware(SessionUserMiddleware):
    
    max_failed_auth_per_ip = 4 # Should be set in settings.SITE?
    # blacklist = {}
    ip_records = {}

    def process_request(self, request):
        super(Middleware, self).process_request(request)
        ip = self.get_client_id(request)
        self.get_ip_record(ip).record_request(request.user.username)
        
    def get_ip_record(self, ip):
        rec = self.ip_records.get(ip, None)
        if rec is None:
            rec = IPRecord(ip)
            self.ip_records[ip] = rec
        return rec
    
    @staticmethod
    def get_client_id(request):
        # from http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # def is_blacklisted(self, ip):
    #     bl = self.blacklist
    #     return bl.get(ip, 0) >= self.max_failed_auth_per_ip

    # def add_to_blacklist(self, ip):
    #     bl = self.blacklist
    #     # ip = self.get_client_id(request)
    #     bl[ip] = bl.get(ip, 0) + 1
    #     logger.info("Bad log-in from IP: %s", ip)

    def authenticate(
            self, username,
            password=NOT_NEEDED,
            request=None, **kwargs):
        ip = self.get_client_id(request)
        rec = self.get_ip_record(ip)
        if rec.blacklisted_since is not None:
            msg = _("Blacklisted IP {} : contact your "
                    "system administrator")
            # raise exceptions.PermissionDenied(msg.format(ip))
            return msg.format(ip)
        msg = super(Middleware, self).authenticate(
            username, password, request, **kwargs)
        if msg:
            rec.login_failures += 1
            if rec.login_failures >= self.max_failed_auth_per_ip:
                # user failed authenticate
                rec.blacklisted_since = datetime.now()
            # self.add_to_blacklist(ip)
        else:
            rec.record_login(username)
        return msg
