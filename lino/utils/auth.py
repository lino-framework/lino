# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

Overview
--------

Lino's authentification utilities

Notes
-----

Notes about marked code locations:

[C1] Before logging the error we must create a `request.user` 
     attribute, otherwise Django might say 
     "AssertionError: The XView middleware requires authentication 
     middleware to be installed."
     
Documented classes and functions
--------------------------------

"""

import os
import logging
logger = logging.getLogger(__name__)


from django.utils import translation
from django.conf import settings
from django import http

from lino.utils import babel
from lino.core.modeltools import resolve_model
from lino.core import perms
from lino.ui import requests as ext_requests

class AnonymousUser(object):
    """
    Similar to Django's approach to represent anonymous visitors 
    as a special kind of user.
    """
    authenticated = False
    email = None
    username = 'anonymous'
    modified = None
    
    def __init__(self):
        try:
            self.profile = perms.UserProfiles.get_by_value(settings.LINO.anonymous_user_profile)
        except KeyError:
            raise Exception(
                "Invalid value %r for `LINO.anonymous_user_profile`. Must be one of %s" % (
                    settings.LINO.anonymous_user_profile,
                    [i.value for i in perms.UserProfiles.items()]))
        


    
class RemoteUserMiddleware(object):
    """
    This does the same as
    `django.contrib.auth.middleware.RemoteUserMiddleware`, 
    but in a simplified manner and without using Sessions.
    
    It also activates the User's language, if that field is not empty.
    Since it will run *after*
    `django.contrib.auth.middleware.RemoteUserMiddleware`
    (at least if you didn't change :meth:`lino.Lino.get_middleware_classes`),
    it will override any browser setting.
    
    """
    
    anonymous_user = None

    def process_request(self, request):
      
        # trigger site startup if necessary
        settings.LINO.startup()
        
        if settings.LINO.user_model:
        
            username = request.META.get(
                settings.LINO.remote_user_header,settings.LINO.default_user)
        else:
          
            username = None
            
        if username:
            """
            20120110 : alicia hatte es geschafft, 
            beim Anmelden ein Leerzeichen vor ihren Namen zu setzen. 
            Apache ließ sie als " alicia" durch.
            Und Lino legte brav einen neuen User " alicia" an.
            """
            username = username.strip()
            
            try:
                request.user = settings.LINO.user_model.objects.get(username=username)
            except settings.LINO.user_model.DoesNotExist,e:
                # [C1]
                request.user = None  
                logger.exception("Unknown username %s from request %s",username, request)
                raise Exception(
                  "Unknown username %r. Please contact your system administrator." 
                  % username)
            
            if len(babel.AVAILABLE_LANGUAGES) > 1:
                #~ lang = settings.LINO.override_user_language() or request.user.language
                lang = request.user.language
                if lang:
                    translation.activate(lang)
                    request.LANGUAGE_CODE = translation.get_language()
                
        else:
          
            if self.anonymous_user is None:
                self.anonymous_user = AnonymousUser()
            request.user = self.anonymous_user
            request.subst_user = None
            
              
        if request.method == 'GET':
            rqdata = request.GET
        elif request.method == 'PUT':
            rqdata = http.QueryDict(request.raw_post_data)
        elif request.method == 'POST':
            rqdata = request.POST
        else: # DELETE
            request.subst_user = None
            request.requesting_panel = None
            return 
        su = rqdata.get(ext_requests.URL_PARAM_SUBST_USER,None)
        if su:
            try:
                su = settings.LINO.user_model.objects.get(id=int(su))
                #~ logger.info("20120714 su is %s",request.subst_user.username)
            except settings.LINO.user_model.DoesNotExist, e:
                pass
        request.subst_user = su
        request.requesting_panel = rqdata.get(ext_requests.URL_PARAM_REQUESTING_PANEL,None)
        
        ul = rqdata.get(ext_requests.URL_PARAM_USER_LANGUAGE,None)
        if ul:
            translation.activate(ul)
            request.LANGUAGE_CODE = translation.get_language()
            
            
                
        
    
