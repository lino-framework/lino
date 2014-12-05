# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""When an exception occurs during an AJAX call, Lino should not
respond with Django's detailed HTML formatted error report but with a
simple traceback.  Because that's more readable when seen in a browser
conseole.  This middleware is automatically being installed on every
Lino site.

Originally inspired by http://djangosnippets.org/snippets/650

Additions by LS:

- also logs a warning on the development server because that is easier
  to read than opening firebug and look at the response.

- must work also when :setting:`DEBUG` is False. Yes, on a production
  server it is not wise to publish the traceback, but our nice HTML
  formatted "Congratulations, you found a problem" page is never the
  right answer to an AJAX call.

"""

from __future__ import unicode_literals

import sys
import traceback
from django.conf import settings
from django.http import HttpResponseServerError
from django.http import HttpResponseForbidden
from django.utils.encoding import smart_text
from django.core.exceptions import PermissionDenied


class AjaxExceptionResponse:

    def process_exception(self, request, exception):
        if request.is_ajax():
            (exc_type, exc_info, tb) = sys.exc_info()
            response = "%s\n" % exc_type.__name__
            response += "%s\n\n" % exc_info
            if settings.DEBUG:
                response += "TRACEBACK:\n"
                for tb in traceback.format_tb(tb):
                    # response += "%r\n" % tb
                    response += smart_text(tb)
                settings.SITE.logger.warning(
                    "AjaxExceptionResponse:\n" + response)
            else:
                settings.SITE.logger.exception(exception)
            if isinstance(exception, PermissionDenied):
                return HttpResponseForbidden(response)
            return HttpResponseServerError(response)
