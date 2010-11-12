## Copyright 2010 Luc Saffre
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

"""
See also :doc:`/tickets/15`
"""

import sys
import logging

def configure(config):
    logger = logging.getLogger('lino')
        
    logger.setLevel(logging.DEBUG)
    
    h = logging.StreamHandler()
    h.setLevel(logging.INFO)
    fmt = logging.Formatter(fmt='%(message)s')
    h.setFormatter(fmt)
    logger.addHandler(h)
    
    if sys.platform == 'win32':
        LOGFILE = 'lino.log'
    else:
        LOGFILE = '/var/log/lino/lino.log'
    if hasattr(logging,'RotatingFileHandler'):
        h = logging.RotatingFileHandler(LOGFILE,maxBytes=10000,backupCount=5)
    else:
        h = logging.FileHandler(LOGFILE)
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
        datefmt='%Y%m-%d %H:%M:%S'
        )
    h.setLevel(logging.DEBUG)
    h.setFormatter(fmt)
    logger.addHandler(h)
    
