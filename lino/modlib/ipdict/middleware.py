# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

from datetime import datetime

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class Middleware(MiddlewareMixin):
    
    def process_request(self, request):
        # super(Middleware, self).process_request(request)
        ip = settings.SITE.plugins.ipdict.get_ip_record(
            request, request.user.username)
        ip.last_request = datetime.now()
        
