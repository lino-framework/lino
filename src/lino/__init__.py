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

#from lino.utils import logger as log

import sys
import logging

#~ if len(logging.root.handlers) == 0:

#logging.basicConfig(level=logging.DEBUG)    

log = logging.getLogger('lino')
    
if len(log.handlers) == 0:
  
    print "Using default logging config"
    
    """
    If you don't like Lino's default logging config, then configure 
    logging in your settings.py before importing lino.
    """
    
    log.setLevel(logging.DEBUG)
    
    if sys.platform == 'win32':
        h = logging.StreamHandler()
        h.setLevel(logging.INFO)
        fmt = logging.Formatter(fmt='%(message)s')
        h.setFormatter(fmt)
        log.addHandler(h)
        
        h = logging.FileHandler('lino.log','w')
        h.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
            datefmt='%Y%m-%d %H:%M:%S'
            )
        h.setFormatter(fmt)
        log.addHandler(h)

    else:
      
        h = logging.FileHandler('/var/log/lino/lino.log','a')
        h.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
            datefmt='%Y%m-%d %H:%M:%S'
            )
        h.setFormatter(fmt)
        log.addHandler(h)
        
        #~ logging.basicConfig(
          #~ format='%(asctime)s %(levelname)s %(module)s : %(message)s',
          #~ datefmt='%Y%m-%d %H:%M:%S',
          #~ level=logging.DEBUG,
          #~ filename='/var/log/lino/lino.log',
          #~ filemode='a',
          #~ )
          
#~ print "log.parent=", log.parent
#~ print "log.manager.disable=", log.manager.disable