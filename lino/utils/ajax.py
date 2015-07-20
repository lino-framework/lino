# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This middleware is automatically being installed on every Lino
site.

When an exception occurs during an AJAX call, Lino should not respond
with Django's default HTML formatted error report but with a
plain-text traceback because that's more readable when seen in a
browser console.

Originally inspired by http://djangosnippets.org/snippets/650

Additions by LS:

- also logs a warning on the development server because that is easier
  to read than opening firebug and look at the response.

- must work also when :setting:`DEBUG` is False. Yes, on a production
  server it is not wise to publish the traceback, but our nice HTML
  formatted "Congratulations, you found a problem" page is never the
  right answer to an AJAX call.

- :func:`format_request` adds information about the incoming call,
  including POST or PUT data.

"""

from __future__ import unicode_literals

import sys
import traceback
from django.conf import settings
from django.http import HttpResponseServerError, QueryDict
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.utils.encoding import smart_text
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


def format_request(request):
    """Format a Django HttpRequest for logging it with the warning when an
    error occurs while processing an AJAX request.

    """
    s = "{0} {1}".format(request.method, request.path)
    qs = request.META.get('QUERY_STRING')
    if qs:
        s += "?" + qs
    if request.body:
        data = QueryDict(request.body)
        data = str(data)
        if len(data) > 1000:
            data = data[:200] + "..."
        s += " (data: {0})".format(data)

    return s


class AjaxExceptionResponse:
    """The middleware class definition."""
    def process_exception(self, request, exception):
        if request.is_ajax():
            (exc_type, exc_info, tb) = sys.exc_info()

            # response to client:
            response = "%s: " % exc_type.__name__
            response += "%s" % exc_info

            # message to be logged:
            msg = "AjaxExceptionResponse {0}\n".format(response)
            msg += "\nin request {0}\n".format(format_request(request))
            msg += "TRACEBACK:\n"
            for tb in traceback.format_tb(tb):
                msg += smart_text(tb)
            if settings.DEBUG:
                settings.SITE.logger.warning(msg)
            else:
                settings.SITE.logger.exception(msg)

            if isinstance(exception, PermissionDenied):
                return HttpResponseForbidden(response)
            if isinstance(exception, ObjectDoesNotExist):
                return HttpResponseBadRequest(response)
            return HttpResponseServerError(response)


