"""
http://djangosnippets.org/snippets/650
"""
import sys, traceback
from django.conf import settings
from django.http import HttpResponseServerError

class AjaxExceptionResponse:
    def process_exception(self, request, exception):
        if settings.DEBUG and request.is_ajax():
            (exc_type, exc_info, tb) = sys.exc_info()
            response = "%s\n" % exc_type.__name__
            response += "%s\n\n" % exc_info
            response += "TRACEBACK:\n"    
            for tb in traceback.format_tb(tb):
                response += "%s\n" % tb
            return HttpResponseServerError(response)
                
                

