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
import datetime
import logging

__version__ = "1.1.2"
"""
Lino version number. 
The latest documented release is :doc:`/releases/20110205`.
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
    
    import pyratemp
    version = getattr(pyratemp,'__version__','')
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

#~ log.info(thanks_to())

#~ from lino.utils.choosers import choices_method, simple_choices_method
#~ from lino.reports import Report
#~ from lino.layouts import DetailLayout


DATE_FORMAT_STRFTIME = '%d.%m.%Y'
DATE_FORMAT_EXTJS = 'd.m.Y'
def PARSE_DATE(s):
    """Convert a string formatted as above to a datetime.date instance.
    See :doc:`/blog/2010/1130`.
    """
    ymd = reversed(map(int,s.split('.')))
    return datetime.date(*ymd)




class LinoSite(object):
    """
    LinoSite base class.
    LinoSite classes are defined and instantiated in Django settings files.
    
    This class is subclassed by :mod:`lino.demos.std.settings`,
    which is subclassed by :mod:`lino.demos.dsbe.settings`
    which is probably subclassed by your local :xfile:`settings.py`
    
    """
    help_url = "http://code.google.com/p/lino"
    #~ index_html = "This is the main page."
    title = "Another Lino Site"
    domain = "www.example.com"
    
    #~ preferred_build_method = 'pisa'
    #~ preferred_build_method = 'appypdf'
    
    csv_params = dict()
    """
    Site-wide default parameters for CSV generation.
    This must be a dictionary that will be used 
    as keyword parameters to Python `csv.writer()
    <http://docs.python.org/library/csv.html#csv.writer>`_
    
    Possible keys include:
    
    - encoding : 
      the charset to use when responding to a CSV request.
      See 
      http://docs.python.org/library/codecs.html#standard-encodings
      for a list of available values.
      
    - many more allowed keys are explained in
      `Dialects and Formatting Parameters
      <http://docs.python.org/library/csv.html#csv-fmt-params>`_.
    
    """
    
    propvalue_max_length = 200
    """
    Used by :mod:`lino.modlib.properties`.
    """
    
    
    def __init__(self):
        #self.django_settings = settings
        #~ self.init_site_config = lambda sc: sc
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None
        # ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined.
        #~ from lino.models import get_site_config
        #~ self.config = get_site_config()
        
    def setup_main_menu(self):
        raise NotImplementedError
          
    def init_site_config(self,sc):
        #~ self.config = sc
        pass
        
    def configure(self,sc):
        self.config = sc
        
    #~ def setup(self):
      
        #~ from lino.models import get_site_config
        #~ self.config = get_site_config()
        
        #~ from lino.site import setup_site
        #~ setup_site(self)

        
    def add_menu(self,*args,**kw):
        return self._menu.add_menu(*args,**kw)

    def context(self,request,**kw):
        d = dict(
          main_menu = menus.MenuRenderer(self._menu,request),
          root_path = self.root_path,
          lino = self,
          settings = settings,
          debug = True,
          #skin = self.skin,
          request = request
        )
        d.update(kw)
        return d
        
    def select_ui_view(self,request):
        html = '<html><body>'
        html += 'Please select a user interface: <ul>'
        for ui in self.uis:
            html += '<li><a href="%s">%s</a></li>' % (ui.name,ui.verbose_name)
        html += '</ul></body></html>'
        return HttpResponse(html)
        
        
    def get_urls(self):
        #~ self.setup()
        assert self._setup_done
        #~ self.setup_ui()
        if len(self.uis) == 1:
            return self.uis[0].get_urls()
        urlpatterns = patterns('',
            ('^$', self.select_ui_view))
        for ui in self.uis:
            urlpatterns += patterns('',
                (ui.name, include(ui.get_urls())),
            )
        return urlpatterns
        #~ return self.ui.get_urls()
        
    def get_site_menu(self,user):
        #~ self.setup()
        assert self._setup_done
        return self._menu.menu_request(user)
        
    #~ def add_program_menu(self):
        #~ return
        #~ m = self.add_menu("app","~Application",)
        #~ m.add_item(url="/accounts/login/",label="Login",can_view=perms.is_anonymous)
        #~ m.add_item(url="/accounts/logout/",label="Logout",can_view=perms.is_authenticated)
        #m.add_item(system.Login(),can_view=perms.is_anonymous)
        #m.add_item(system.Logout(),can_view=perms.is_authenticated)
        
    def setup_dblogger(self,logger):
        """
        Called when settings.DBLOGFILE is not empty *and* a logger 'db' 
        hasn't been configured manually.
        See :mod:`lino.utils.dblogger`
        """
        logger.setLevel(logging.INFO)
      




