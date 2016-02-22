# -*- coding: UTF-8 -*-
# Copyright 2010-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""

Lino's authentification middleware


"""

from __future__ import unicode_literals
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.core import exceptions
from django.utils import translation
from django.utils.timezone import activate
from django.conf import settings
from django import http

from lino.core import constants
from lino.modlib.users.utils import AnonymousUser


class AuthMiddleWareBase(object):
    """Common base class for :class:`RemoteUserMiddleware`,
    :class:`SessionUserMiddleware` and :class:`NoUserMiddleware`.

    """

    # Singleton instance
    _instance = None

    class NOT_NEEDED(object):
        pass

    def __init__(self):
        # Save singleton instance
        AuthMiddleWareBase._instance = self
        # print("20150129 Middleware is {0}".format(self.__class__))

    def get_user_from_request(self, request):
        raise NotImplementedError

    def process_request(self, request):
        # first request will trigger site startup to load UserProfiles
        # settings.SITE.startup()

        user = self.get_user_from_request(request)

        # logger.info("20150428 %s process_request %s -> %s" % (
        #     self.__class__.__name__, request.path, user))

        self.on_login(request, user)

    def authenticate(self, username, password=NOT_NEEDED):
        # logger.info("20150424 authenticate %s, %s" % (username, password))

        if not username:
            return AnonymousUser.instance()

        # 20120110 : Alicia once managed to add a space char in front
        # of her username log in the login dialog.  Apache let her in
        # as " alicia".
        username = username.strip()

        try:
            user = settings.SITE.user_model.objects.get(username=username)
            if user.profile is None:
                logger.info(
                    "Could not authenticate %s : user has no profile",
                    username)
                return None
            if password != self.NOT_NEEDED:
                if not user.check_password(password):
                    logger.info(
                        "Could not authenticate %s : password mismatch",
                        username)
                    return None
                #~ logger.info("20130923 good password for %s",username)
            #~ else:
                #~ logger.info("20130923 no password needed for %s",username)
            return user
        except settings.SITE.user_model.DoesNotExist:
            logger.debug("Could not authenticate %s : no such user", username)
            return None

    def on_login(self, request, user):
        """The method which is applied when the user has been determined.  On
        multilingual sites, if URL_PARAM_USER_LANGUAGE is present it
        overrides user.language.

        """
        # logger.info("20130923 on_login(%s)" % user)

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

    def can_change_password(self, request, user):
        return False

    def change_password(self, request, user, password):
        raise NotImplementedError


class DefaultUserMiddleware(AuthMiddleWareBase):
    """Used when :attr:`lino.core.site.Site.default_user` is non-empty.
    """
    def get_user_from_request(self, request):
        user = self.authenticate(settings.SITE.default_user)

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

        user = self.authenticate(username)

        # print 20150701, user.profile.role

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

        user = self.authenticate(request.session.get('username'),
                                 request.session.get('password'))

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
        from activedirectory import Client, Creds
        from activedirectory.core.exception import Error

        server_spec = settings.SITE.ldap_auth_server
        if isinstance(server_spec, basestring):
            server_spec = server_spec.split()

        self.domain = server_spec[0]
        self.server = server_spec[1]

        self.creds = Creds(domain)

    def check_password(self, username, password):

        try:
            self.creds.acquire(username, password, server=self.server)
            return True
        except Exception as e:
            pass

        return False

    def authenticate(self, username, password=SessionUserMiddleware.NOT_NEEDED, from_session=False):
        if not from_session and username and password != SessionUserMiddleware.NOT_NEEDED:
            if not self.check_password(username, password):
                return None

        return SessionUserMiddleware.authenticate(username, SessionUserMiddleware.NOT_NEEDED)

    def get_user_from_request(self, request):

        user = self.authenticate(request.session.get('username'),
                                 request.session.get('password'), True)

        if user is None:
            logger.debug("Login failed from session %s", request.session)
            user = AnonymousUser.instance()

        return user


def get_auth_middleware():
    """
    Returns active Authentication Middleware instance

    :return: AuthMiddleWareBase
    """
    return AuthMiddleWareBase._instance


def authenticate(*args, **kwargs):
    """
    Needed by the ``/auth`` view (:class:`lino.ui.views.Authenticate`).
    Called when the Login window of the web interface is confirmed.
    """
    return get_auth_middleware().authenticate(*args, **kwargs)
