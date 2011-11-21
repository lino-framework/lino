# -*- coding: UTF-8 -*-
import logging

unicode_string = u"Татьяна"
utf8_string = "'Татьяна' is an invalid string value"

logging.warning(unicode_string)
logging.warning(utf8_string)

try:
    raise Exception(utf8_string)
except Exception,e:
  
    print "--- (Log a traceback of the exception):"
    logging.exception(e)
    
    print "--- Everything okay until here, but now we run into trouble:"
    logging.warning(u"1 Deferred %s : %s",unicode_string,e)
    logging.warning(u"2 Deferred %s : %s",unicode_string,utf8_string)
    
    print "--- some workarounds:"
    logging.warning(u"3 Deferred %s : %s",unicode_string,utf8_string.decode('UTF-8'))
    from django.utils.encoding import force_unicode
    logging.warning(u"4 Deferred %s : %s",unicode_string,force_unicode(utf8_string))
