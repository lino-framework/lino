# -*- coding: UTF-8 -*-
# Copyright 2010-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""

Lino's authentification middleware


"""

raise Exception("No longer used after 20170708")

from __future__ import unicode_literals
import six
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.core import exceptions
from django.utils import translation
from django.utils.timezone import activate
from django.conf import settings
from django import http
from django.utils.translation import ugettext_lazy as _

from lino.core import constants
from lino.modlib.users.utils import AnonymousUser

class NOT_NEEDED(object):
    pass


class AuthMiddleWareBase(object):
    """Common base class for :class:`RemoteUserMiddleware`,
    :class:`SessionUserMiddleware` and :class:`NoUserMiddleware`.

    """

    # Singleton instance
    _instance = None
    
    def __init__(self):
        # Save singleton instance
        AuthMiddleWareBase._instance = self
        # print("20150129 Middleware is {0}".format(self.__class__))

    def process_request(self, request):
        # first request will trigger site startup to load UserTypes
        # settings.SITE.startup()

        user = self.get_user_from_request(request)

        # logger.info("20150428 %s process_request %s -> %s" % (
        #     self.__class__.__name__, request.path, user))
        
        request.user = user
        
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
        #~ logger.info("20121228 subst_user is %r",request.subst_user)
        #~ if request.subst_user is not None and not isinstance(request.subst_user,settings.SITE.user_model):
            #~ raise Exception("20121228")

    def get_user_from_request(self, request):
        raise NotImplementedError()

    def lookup_user_by_name(self, username):
        if not username:
            return None
        # 20120110 : Alicia once managed to add a space char in front
        # of her username log in the login dialog.  Apache let her in
        # as " alicia".
        username = username.strip()
        try:
            return settings.SITE.user_model.objects.get(username=username)
        except settings.SITE.user_model.DoesNotExist:
            return None
            # logger.debug("Could not authenticate %s : no such user",
            #              username)
        # return None


    def authenticate(self, username, password=NOT_NEEDED, request=None):
        """Authenticate the given username and password and request.

        Return None if authentication is successfull, otherwise a
        translatable message to be forwarded to the user who is trying
        to authenticate.

        """
        # logger.info("20150424 authenticate %s, %s" % (username, password))

        user = self.lookup_user_by_name(username)
        
        if user is None:
            return _("Could not authenticate {} : no such user").format(
                username)
            # return AnonymousUser.instance()
        

        if user.profile is None:
            return _(
                "Could not authenticate {} : user is inactive").format(
                    username)
            return None
        if password is NOT_NEEDED:
            return
        
        if not user.check_password(password):
            return _(
                "Could not authenticate {} : wrong password").format(
                    username)

    def can_change_password(self, request, user):
        return False

    def change_password(self, request, user, password):
        raise NotImplementedError

class DefaultUserMiddleware(AuthMiddleWareBase):
    """Used when :attr:`lino.core.site.Site.default_user` is non-empty.
    """
    def get_user_from_request(self, request):
        user = self.lookup_user_by_name(settings.SITE.default_user)

        # print 20150701, user.profile.role

        if user is None:
            # print("20130514 Unknown username %s from request %s" % (
            #     username, request))
            #~ raise Exception(
            #~ raise exceptions.PermissionDenied("Unknown or inactive username %r. Please contact your system administrator."
            # logger.info("Unknown or inactive username %r.", username)
            raise exceptions.PermissionDenied(
                "default_user {0} does not exist".format(
                    settings.SITE.default_user))

        return user


class RemoteUserMiddleware(AuthMiddleWareBase):

    """Middleware automatically installed by :meth:`get_middleware_classes
    <lino.core.site.Site.get_middleware_classes>` when both
    :attr:`remote_user_header
    <lino.core.site.Site.remote_user_header>` and
    :attr:`user_model <lino.core.site.Site.user_model>` are not
    empty.
    
    This does the same as
    `django.contrib.auth.middleware.RemoteUserMiddleware`, but in a
    simplified manner and without using Sessions.
    
    It also activates the User's language, if that field is not empty.
    Since it will run *after*
    `django.contrib.auth.middleware.RemoteUserMiddleware`
    (at least if you didn't change :meth:`lino.Lino.get_middleware_classes`),
    it will override any browser setting.

    """

    def get_user_from_request(self, request):
        username = request.META.get(settings.SITE.remote_user_header, None)
        if not username:
            raise Exception(
                "Using remote authentication, but no user credentials found.")

        user = self.lookup_user_by_name(username)

        if user is None:
            # print("20130514 Unknown username %s from request %s" % (
            #     username, request))
            #~ raise Exception(
            #~ raise exceptions.PermissionDenied("Unknown or inactive username %r. Please contact your system administrator."
            # logger.info("Unknown or inactive username %r.", username)
            raise exceptions.PermissionDenied()

        return user


class NoUserMiddleware(AuthMiddleWareBase):

    """Middleware automatically installed by
    :meth:`lino.core.site.Site.get_middleware_classes` when
    :attr:`lino.core.site.Site.user_model` is None.

    """

    def get_user_from_request(self, request):
        return AnonymousUser.instance()


class SessionUserMiddleware(AuthMiddleWareBase):

    """Middleware automatically installed by
    :meth:`get_middleware_classes
    <lino.site.Site.get_middleware_classes>` when
    :setting:`remote_user_header` is None and :setting:`user_model`
    not.

    """

    def get_user_from_request(self, request):

        # logger.info("20150428 %s get_user_from_request %s, %s" % (
        #     self.__class__.__name__,
        #     request.session.get('username'),
        #     request.session.get('password')))

        user = self.lookup_user_by_name(request.session.get('username'))
        if user is None:
            user = AnonymousUser.instance()
        return user


class LDAPAuthMiddleware(SessionUserMiddleware):

    """
    Middleware automatically installed by 
    :meth:`get_middleware_classes <lino.site.Site.get_middleware_classes>`
    when 
    
    - :setting:`user_model` is not None
    - :setting:`remote_user_header` is None
    - :setting:`ldap_auth_server` is not None
    
    Using this requires 
    `activedirectory <https://github.com/theatlantic/python-active-directory>`_.
    
    Thanks to Josef Kejzlar for the initial implementation.
    
    """

    def __init__(self):
        from activedirectory import Creds
        # from activedirectory.core.exception import Error

        server_spec = settings.SITE.ldap_auth_server
        if isinstance(server_spec, six.string_types):
            server_spec = server_spec.split()

        domain = server_spec[0]
        self.server = server_spec[1]
        self.creds = Creds(domain)

    def authenticate(
            self,
            username,
            password=NOT_NEEDED,
            request=None):
        if username and password is not NOT_NEEDED:
            try:
                self.creds.acquire(username, password, server=self.server)
            except Exception as e:
                return str(e)
        return SessionUserMiddleware.authenticate(
            username, password=NOT_NEEDED, request=request)

    # def get_user_from_request(self, request):
    #     user = self.lookup_user_by_name(request.session.get('username'))
    #     if user is None:
    #         # logger.debug("Login failed from session %s", request.session)
    #         user = AnonymousUser.instance()

    #     return user


def get_auth_middleware():
    """
    Returns active Authentication Middleware instance

    :return: AuthMiddleWareBase
    """
    return AuthMiddleWareBase._instance


def authenticate(username, password, request):
    """
    Needed by the ``/auth`` view (:class:`lino.ui.views.Authenticate`).
    Called when the Login window of the web interface is confirmed.
    """
    return get_auth_middleware().authenticate(username, password, request)
