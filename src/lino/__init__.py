## Copyright 2002-2009 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

__micro__ = 1

__version__ = "0.8.%d" % __micro__

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.saffre-rumma.ee"

__copyright__ = """\
Copyright (c) 2002-2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

import logging

#_log_level = logging.WARNING
_log_level = logging.INFO
#_log_level = logging.DEBUG


if len(logging.root.handlers) == 0:
    
    """
    
    Lino's default logging behaviour is to render the bare messages 
    to sys.stderr and write complete records (including timestamp, name, level) to a file lino.log.
    If you don't like this, then just configure logging before instantiating LinoSite.
    
    """
    
    # this will create a first handler in the logging.root logger:
    logging.basicConfig(format='%(message)s',level=_log_level)
    
    if True:
        h = logging.FileHandler('lino.log','w')
        h.setLevel(_log_level)
        fmt = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(module)s : %(message)s ',
            datefmt='%Y%m-%d %H:%M')
        h.setFormatter(fmt)
        logging.root.addHandler(h)

log = logging.getLogger('lino')
    
    #~ if True:
        #~ h = logging.root.handlers[0]
        #~ #h = logging.StreamHandler(sys.stdout)
        #~ #h.setLevel(logging.INFO)
        #~ formatter = logging.Formatter('%(message)s')
        #~ #formatter = logging.Formatter('%(levelname)s %(message)s')
        #~ h.setFormatter(formatter)
        #~ self.log.addHandler(h)

    
#~ else:
    #~ self.log = logging.getLogger('lino')
    
#print self.log.handlers
#print "foo"

