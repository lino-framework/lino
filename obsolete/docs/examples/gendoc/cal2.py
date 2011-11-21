"""

Uses the calendar and pdfprn modules to create a printable calendar
that fills an A4 page.

"""

import sys
import calendar
import datetime

from lino.textprinter.pdfprn import PdfTextPrinter

import locale
locale.setlocale(locale.LC_ALL, '')


#cal=calendar.LocaleTextCalendar(locale=locale.getdefaultlocale()) #locale=options.locale)

cal=calendar.TextCalendar()

s=cal.formatyear(datetime.date.today().year,w=4,l=2)

# surprise: formatyear() doesn't return a unicode string:
s=s.decode(sys.getfilesystemencoding())

#print s



p=PdfTextPrinter("tmp.pdf",margin="3mm")
p.setOrientationLandscape()
p.setCpi(10)
p.setLpi(9)
for ln in s.splitlines():
    p.writeln(ln)

p.close()
