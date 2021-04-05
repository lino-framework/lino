# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# This started as a copy of Django 1.11 django.contrib.auth.middleware.

import datetime

from django.core import exceptions
from django.utils import translation
from django.utils.timezone import activate
from django.conf import settings
from django import http

from lino.core import constants
from .utils import AnonymousUser

from lino.utils import get_client_ip_address
from lino.core import auth
from lino.core.auth import load_backend
from .backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

ACTIVITY_SLOT = datetime.timedelta(seconds=10)
# time to wait before we update last_activity in session

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
                                                "Requires session middleware "
                                                "to be installed. Edit your MIDDLEWARE%s setting to insert "
                                                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                                                "'django.contrib.auth.middleware.AuthenticationMiddleware'."
                                            ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))


class RemoteUserMiddleware(MiddlewareMixin):
    """
    Middleware for utilizing Web-server-provided authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.

    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"
    force_logout_if_no_header = True

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(request, remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        # LS 20171221 : support remote auth without session
        backend_str = request.session.get(auth.BACKEND_SESSION_KEY, '')
        if backend_str:
            backend = auth.load_backend(backend_str)
            try:
                username = backend.clean_username(username)
            except AttributeError:  # Backend has no clean_username method.
                pass
        return username

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, RemoteUserBackend):
                auth.logout(request)


def request2data(request, user_language=None):
    if request.method == 'GET':
        rqdata = request.GET
    elif request.method in ('PUT', 'DELETE'):
        # raw_post_data before Django 1.4
        rqdata = http.QueryDict(request.body)
    elif request.method == 'POST':
        rqdata = request.POST
    else:
        # e.g. OPTIONS, HEAD
        if user_language and len(settings.SITE.languages) > 1:
            translation.activate(user_language)
            request.LANGUAGE_CODE = translation.get_language()
        # ~ logger.info("20121205 on_login %r",translation.get_language())
        request.requesting_panel = None
        request.subst_user = None
        return
        # ~ else: # DELETE
        # ~ request.subst_user = None
        # ~ request.requesting_panel = None
        # ~ return

    request.requesting_panel = rqdata.get(
        constants.URL_PARAM_REQUESTING_PANEL, None)
    request.device_type = rqdata.get(
        constants.URL_PARAM_DEVICE_TYPE, settings.SITE.device_type)

    if len(settings.SITE.languages) > 1:
        user_language = rqdata.get(
            constants.URL_PARAM_USER_LANGUAGE, user_language)
        if user_language:
            translation.activate(user_language)
        request.LANGUAGE_CODE = translation.get_language()

    return rqdata


class NoUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.USE_TZ:
            activate(settings.SITE.models.about.TimeZones.default.tzinfo)
        request.subst_user = None
        request.device_type = None
        request.user = AnonymousUser()
        request2data(request)


class WithUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        user_language = user.language  # or settings.SITE.get_default_language()

        if settings.USE_TZ:
            if user.time_zone:
                activate(user.time_zone.tzinfo)
            else:
                activate(settings.SITE.models.about.TimeZones.default.tzinfo)

        if user.is_anonymous:
            request.subst_user = None
            request.requesting_panel = None
            return
        update = False
        now = datetime.datetime.now()
        last = request.session.get('last_activity', None)
        if last is None:
            update = True
        else:
            last = datetime.datetime.strptime(last, "%Y-%m-%dT%H:%M:%S.%f")
            if now - last > ACTIVITY_SLOT:
                # print("20210116 update last activity")
                update = True
        if update:
            # information shown in users.ActiveSessions
            request.session['last_activity'] = now.isoformat()
            request.session['last_ip_addr'] = get_client_ip_address(request)

        rqdata = request2data(request, user_language)
        if rqdata is None:
            return

        su = rqdata.get(constants.URL_PARAM_SUBST_USER, None)
        if su is not None:
            if su:
                try:
                    su = settings.SITE.user_model.objects.get(id=int(su))
                    # ~ logger.info("20120714 su is %s",su.username)
                except settings.SITE.user_model.DoesNotExist:
                    su = None
            else:
                su = None  # e.g. when it was an empty string "su="
        request.subst_user = su



# class DeviceTypeMiddleware(MiddlewareMixin):
#     """Sets the `device_type` attribute on every incoming request.
#     """
#     def process_request(self, request):
#         user = request.user
#         user_language = user.language  # or settings.SITE.get_default_language()
#         rqdata = request2data(request, user_language)
#         if rqdata is None:
#             return
#
#         dt = rqdata.get(
#             constants.URL_PARAM_DEVICE_TYPE, settings.SITE.device_type)
#         request.device_type = dt
