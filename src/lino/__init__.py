__all__ = []

__docformat__ = 'reStructuredText'

__version__ = "0.6.5"

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.sourceforge.net"


__copyright__ = """\
Lino version %s.
Copyright (c) 2002-2005 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" % __version__

import sys
__credits__ = "Python %d.%d.%d %s\n" % sys.version_info[0:4]

try:
    import wx
    __credits__ += "wxPython " + wx.__version__ + "\n"
except ImportError:
    pass

try:
    import sqlite
    __credits__ += "PySQLLite " + sqlite.version + "\n"
except ImportError:
    pass
    
try:
    import reportlab
    __credits__ += "The Reportlab PDF generation library " + \
                   reportlab.Version + "\n"
except ImportError:
    pass
        

try:
    import win32print
    __credits__ += "Python Windows Extensions " + "\n"
except ImportError:
    pass

