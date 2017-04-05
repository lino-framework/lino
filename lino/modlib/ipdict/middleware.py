# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre.
# License: BSD, see LICENSE for more details.

#import six
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
# from django.contrib.humanize.templatetags.humanize import naturaltime
from django.conf import settings

from lino.core.auth import NOT_NEEDED, SessionUserMiddleware

# def format_timestamp(dt):        
#     d = dt.strftime(settings.SITE.date_format_strftime)
#     t = dt.strftime(settings.SITE.time_format_strftime)
#     return "{} {}".format(d, t)

max_blacklist_time  = timedelta(minutes=1)

class IPRecord(object):
    def __init__(self, addr, username):
        self.addr = addr
        self.username = username
        self.login_failures = 0
        self.blacklisted_since = None
        self.last_login = None
        self.last_failure = None
        self.last_request = None

#six.python_2_unicode_compatible
class UserIPRecord(object):
    def __init__(self, ip, username):
        self.ip = ip

    # def __str__(self):
    #     s = u"{username} {last_request} ({ago})".format(
    #         username=self.username,
    #         last_request=format_timestamp(self.last_request),
    #         ago=naturaltime(self.last_request)
    #     )
    #     # idletime = datetime.now() - self.last_request
    #     # if idletime > max_idletime:
    #     #     s += _(" ({})").format(naturaltime(self.last_request))
    #     return s
    
class Middleware(SessionUserMiddleware):
    
    max_failed_auth_per_ip = 4 # Should be set in settings.SITE?
    # blacklist = {}
    ip_records = {}
        
    def process_request(self, request):
        super(Middleware, self).process_request(request)
        ip = self.get_ip_record(request, request.user.username)
        ip.last_request = datetime.now()
        
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
        rec = self.get_ip_record(request, 'anonymous')
        if rec.blacklisted_since is not None:
            since = datetime.now() - rec.blacklisted_since
            if since < max_blacklist_time:
                msg = _("Blacklisted IP {} : contact your "
                        "system administrator")
                # raise exceptions.PermissionDenied(msg.format(ip))
                return msg.format(rec.addr)
        msg = super(Middleware, self).authenticate(
            username, password, request, **kwargs)
        if msg:
            # user failed to authenticate
            rec.login_failures += 1
            if rec.login_failures >= self.max_failed_auth_per_ip:
                # maybe a robot is trying to log in with brute force
                # and waited patiently for max_blacklist_time to pass,
                # and now continues to try. In that case we don't
                # forget the blacklisted_since, so the robot must now
                # wait a full minute for every attempt
                if rec.blacklisted_since is None:
                    rec.blacklisted_since = datetime.now()
            # self.add_to_blacklist(ip)
        else:
            # when an IP was blacklisted, got unlocked after
            # max_blacklist_time and then received a successful login,
            # then all sins of anonymous are being erased:
            rec.blacklisted_since = None
            rec.login_failures = 0
            
            # record the login time for username
            rec = self.get_ip_record(request, username)
            rec.last_login = datetime.now()
        return msg
