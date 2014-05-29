# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""Originally inspired by http://djangosnippets.org/snippets/650

Additions by LS:

- also logs a warning on the development server because that is easier
  to read than opening firebug and look at the response.

- must work also when :setting:`DEBUG` is False. Yes, on a production
  server it is not wise to publish the traceback, but our nice HTML
  formatted "Congratulations, you found a problem" page is never the
  right answer to an AJAX call.

"""

import sys
import traceback
from django.conf import settings
from django.http import HttpResponseServerError


class AjaxExceptionResponse:

    def process_exception(self, request, exception):
        if request.is_ajax():
            (exc_type, exc_info, tb) = sys.exc_info()
            response = "%s\n" % exc_type.__name__
            response += "%s\n\n" % exc_info
            if settings.DEBUG:
                response += "TRACEBACK:\n"
                for tb in traceback.format_tb(tb):
                    #~ response += "%s\n" % tb
                    response += tb
            # import logging
            # logger = logging.getLogger(__name__)
            settings.SITE.logger.warning("AjaxExceptionResponse:\n" + response)
            return HttpResponseServerError(response)
