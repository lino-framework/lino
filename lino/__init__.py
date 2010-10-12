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

__version__ = "0.8.8"

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
    To bypass Lino's default logging config, just configure 
    logging yourself before importing lino.
    """
    
    log.setLevel(logging.DEBUG)
    
    h = logging.StreamHandler()
    h.setLevel(logging.INFO)
    fmt = logging.Formatter(fmt='%(message)s')
    h.setFormatter(fmt)
    log.addHandler(h)
    
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
    log.addHandler(h)
    
    if False:
        
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
            # 20100913 A separate lino.log is not necessary
            # Assuming we are under mod_wsgi, we just write to sys.stderr which goes to the web server's error log
            # Thanks to adroffner on http://djangosnippets.org/snippets/1731/
            if False:
                fmt = logging.Formatter(
                    fmt='%(asctime)s %(levelname)s %(module)s : %(message)s',
                    datefmt='%Y%m-%d %H:%M:%S'
                    )

                if hasattr(logging,'RotatingFileHandler'):
                    h = logging.RotatingFileHandler('/var/log/lino/lino.log',maxBytes=10000,backupCount=5)
                else:
                    h = logging.FileHandler('/var/log/lino/lino.log')
                h.setLevel(logging.DEBUG)
                h.setFormatter(fmt)
                log.addHandler(h)
            
            h = logging.StreamHandler(sys.stderr) 
            fmt = logging.Formatter(fmt='%(levelname)s %(module)s : %(message)s')
            h.setFormatter(fmt)
            h.setLevel(logging.DEBUG)
            log.addHandler(h)
        

def thanks_to(all=True):
    yield ("Lino", __version__, __url__)
    if all:
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python",version,"http://www.python.org/")
        
        import reportlab
        yield ("ReportLab Toolkit",reportlab.Version, "http://www.reportlab.org/rl_toolkit.html")
                   
        import yaml
        version = getattr(yaml,'__version__','')
        yield ("PyYaml",version,"http://pyyaml.org/")
        
        import dateutil
        version = getattr(dateutil,'__version__','')
        yield ("python-dateutil",version,"http://labix.org/python-dateutil")
        
        try:
            import ho.pisa as pisa
            version = getattr(pisa,'__version__','')
            yield ("xhtml2pdf",version,"http://www.xhtml2pdf.com")
        except ImportError:
            pass
    

#~ log.info(thanks_to())

#~ from lino.utils.choosers import choices_method, simple_choices_method
#~ from lino.reports import Report
#~ from lino.layouts import DetailLayout
