## Copyright 2002-2010 Luc Saffre
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

import sys
import logging

__version__ = "0.8.2"

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://code.google.com/p/lino/"

__copyright__ = """\
Copyright (c) 2002-2010 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""


if False: 
    """
    subprocess.Popen() took very long and even got stuck on Windows XP.
    I didn't yet explore this phenomen more.
    """
    # Copied from Sphinx <http://sphinx.pocoo.org>
    from os import path
    package_dir = path.abspath(path.dirname(__file__))
    if '+' in __version__ or 'pre' in __version__:
        # try to find out the changeset hash if checked out from hg, and append
        # it to __version__ (since we use this value from setup.py, it gets
        # automatically propagated to an installed copy as well)
        try:
            import subprocess
            p = subprocess.Popen(['hg', 'id', '-i', '-R',
                                  path.join(package_dir, '..', '..')],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                __version__ += ' (Hg ' + out.strip() +')'
            #~ if err:
                #~ print err
        except Exception:
            pass



log = logging.getLogger('lino')
    
if len(log.handlers) == 0:
  
    #~ print "Using default logging config"
    
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
      
        h = logging.FileHandler('/var/log/lino/lino.log','w')
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



