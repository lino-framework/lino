# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
import six
from builtins import object

from django.core import exceptions
from django.utils import translation
from django.utils.timezone import activate
from django.conf import settings
from django import http

from lino.core import constants

class Middleware(object):
    
    def process_request(self, request):
        request.subst_user = None
        user = request.user
        user_language = user.language  # or settings.SITE.get_default_language()

        if settings.USE_TZ:
            activate(user.timezone or settings.TIME_ZONE)

        if request.method == 'GET':
            rqdata = request.GET
        elif request.method in ('PUT', 'DELETE'):
            # raw_post_data before Django 1.4
            rqdata = http.QueryDict(request.body)
        elif request.method == 'POST':
            rqdata = request.POST
        else:
            # e.g. OPTIONS, HEAD
            if len(settings.SITE.languages) > 1:
                if user_language:
                    translation.activate(user_language)
                request.LANGUAGE_CODE = translation.get_language()
            #~ logger.info("20121205 on_login %r",translation.get_language())
            request.requesting_panel = None
            request.subst_user = None
            return
        # ~ else: # DELETE
            #~ request.subst_user = None
            #~ request.requesting_panel = None
            #~ return

        if len(settings.SITE.languages) > 1:

            user_language = rqdata.get(
                constants.URL_PARAM_USER_LANGUAGE, user_language)
            if user_language:
                translation.activate(user_language)
            request.LANGUAGE_CODE = translation.get_language()

        su = rqdata.get(constants.URL_PARAM_SUBST_USER, None)
        if su is not None:
            if su:
                try:
                    su = settings.SITE.user_model.objects.get(id=int(su))
                    #~ logger.info("20120714 su is %s",su.username)
                except settings.SITE.user_model.DoesNotExist:
                    su = None
            else:
                su = None  # e.g. when it was an empty string "su="
        request.subst_user = su
        request.requesting_panel = rqdata.get(
            constants.URL_PARAM_REQUESTING_PANEL, None)

