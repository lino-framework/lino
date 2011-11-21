# -*- coding: UTF-8 -*-
import sys
import os
import locale


def babel_message():

    s = u"""
    
Some sentences in different languages:

    Ännchen Müller isst gern süße Soßen.
    Cède à César les pâturages reçues.
    Tõesti, ma ütlen teile, see ei ole ükskõik.

Overview table with some accented characters:

        A E I O U   a e i o u
    ¨   Ä Ë Ï Ö Ü   ä ë ï ö ü
    ~   Ã . . Õ .   ã . . õ .
    ´   Á É Í Ó Ú   á é í ó ú
    `   À È Ì Ò Ù   à è ì ò ù
    ^   Â Ê Î Ô Û   â ê î ô û
    
    
"""
    
    try:
        out_encoding=repr(sys.stdout.encoding)
    except AttributeError:
        out_encoding="(undefined)"
        
    try:
        in_encoding=repr(sys.stdin.encoding)
    except AttributeError:
        in_encoding="(undefined)"

    try:
        nl_langinfo=repr(locale.nl_langinfo(locale.CODESET))
    except AttributeError:
        nl_langinfo="(undefined)"

    s+="""
    
Some system settings related to encodings:

    locale.getdefaultlocale()   : %r
    sys.getdefaultencoding()    : %r
    sys.getfilesystemencoding() : %r
    sys.stdout.encoding         : %s
    sys.stdin.encoding          : %s
    locale codeset              : %s""" % ( 
      locale.getdefaultlocale(), 
      sys.getdefaultencoding(),
      sys.getfilesystemencoding(),
      out_encoding,
      in_encoding,
      nl_langinfo)

    func = getattr(locale,'nl_langinfo',None)
    if func: # nl_langinfo not available on win32
        s += """
    locale codeset  : """ + func(locale.CODESET)
    return s
              


print babel_message()



#~ locale.setlocale(locale.LC_ALL, '')

#~ print "encodings"
#~ print "---------"

#~ print "defaultencoding     :", sys.getdefaultencoding()
#~ print "filesystemencoding  :", sys.getfilesystemencoding()
#~ print "sys.stdout.encoding :", sys.stdout.encoding

#~ print u"Ännchen Müller aß gern süße Soßen."
#~ fn = u'\xfc'
#~ fn = u'ü'

#~ fn = u'Liste_F\xfchrerschein.pdf'
#~ print fn

#~ os.stat(fn)