## Copyright 2002-2011 Luc Saffre
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
Lino is a Python package to be used on Django sites.
See :doc:`/admin/install` on how to use it.

"""

import sys
import logging

__version__ = "1.1.11"
"""
Lino version number. 
The latest documented release is :doc:`/releases/20110429`.
"""

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"

__copyright__ = """\
Copyright (c) 2002-2011 Luc Saffre.
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


NOT_FOUND_MSG = '(not installed)'

def using():
    """
    Yields a list of third-party software descriptors used by Lino.
    Each descriptor is a tuple (name, version, url).
    
    """
    import sys
    version = "%d.%d.%d" % sys.version_info[:3]
    yield ("Python",version,"http://www.python.org/")
    
    import django
    yield ("Django",django.get_version(),"http://www.djangoproject.com")
    
    import dateutil
    version = getattr(dateutil,'__version__','')
    yield ("python-dateutil",version,"http://labix.org/python-dateutil")
    
    try:
        import Cheetah
        version = Cheetah.Version 
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("Cheetah",version ,"http://cheetahtemplate.org/")

    try:
        import docutils
        version = docutils.__version__
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("docutils",version ,"http://docutils.sourceforge.net/")

    import yaml
    version = getattr(yaml,'__version__','')
    yield ("PyYaml",version,"http://pyyaml.org/")
    
    try:
        import pyratemp
        version = getattr(pyratemp,'__version__','')
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("pyratemp",version,"http://www.simple-is-better.org/template/pyratemp.html")
    
    try:
        import ho.pisa as pisa
        version = getattr(pisa,'__version__','')
        yield ("xhtml2pdf",version,"http://www.xhtml2pdf.com")
    except ImportError:
        pass

    import reportlab
    yield ("ReportLab Toolkit",reportlab.Version, "http://www.reportlab.org/rl_toolkit.html")
               
    try:
        #~ import appy
        from appy import version
        version = version.verbose
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("appy.pod",version ,"http://appyframework.org/pod.html")


def welcome_text():
    return "Lino version %s using %s" % (
      __version__, 
      ', '.join(["%s %s" % (n,v) for n,v,u in using()]))

def welcome_html():
    return "Lino version %s using %s" % (
      __version__,
      ', '.join(['<a href="%s" target="_blank">%s</a> %s' % (u,n,v) for n,v,u in using()]))


