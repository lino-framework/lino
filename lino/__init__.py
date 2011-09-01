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

import os
import sys
import datetime
from tempfile import gettempdir
from os.path import join, abspath, dirname, normpath
import logging

__version__ = "1.2.2"
"""
Lino version number. 
The latest released version is :doc:`/releases/20110727`.
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
    
    if False:
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


class Lino(object):
    """
    Base class for the Lino Application instance stored in :setting:`LINO`.
    
    Subclasses of this can be defined and instantiated in Django settings files.
    
    This class is first defined in :mod:`lino`, then subclassed by 
    :mod:`lino.apps.dsbe.settings` or 
    :mod:`lino.apps.igen.settings`,
    which is imported into your local :xfile:`settings.py`,
    where you may subclass it another time.
    
    To use your subclass, you must instantiate it and store the instance 
    in the :setting:`LINO` variable of your :xfile:`settings.py`::
    
      LINO = Lino(__file__,globals())
      
    With the parameters `__file__` and `globals()` you give Lino information 
    about your local settings. 
    Lino will also adapt the settings FIXTURE_DIRS, MEDIA_ROOT and TEMPLATE_DIRS 
    for you.
    
    """
    
    auto_makeui = True
    """
    useful when debugging directly on the generated `lino.js`
    """
    
    root_url = '' # 
    """
    must begin with a slash if not empty
    See also  
    http://groups.google.com/group/django-users/browse_thread/thread/c95ba83e8f666ae5?pli=1
    http://groups.google.com/group/django-users/browse_thread/thread/27f035aa8e566af6
    """
    
    extjs_root = None
    """Path to the extjs root directory. Only to be used on a development server."""
    tinymce_root = None
    """Path to the tinymce root directory. Only to be used on a development server."""
    
    allow_duplicate_cities = False
    """Set this to True if that's what you want. 
    In normal situations you shouldn't, but one exception is here :doc:`/blog/2011/0830`
    """
    
    
    help_url = "http://code.google.com/p/lino"
    #~ index_html = "This is the main page."
    title = "Untitled Lino Application"
    #~ domain = "www.example.com"
    
    uid = 'myuid'
    """
    A universal identifier for this Lino site. 
    This is needed when synchronizing with CalDAV server.  
    Locally created calendar components in remote calendars 
    will get a UID based on this parameter,
    using ``"%s@%s" (self.pk,settings.LINO.ui)``.
    
    The default value is ``'myuid'``, and
    you should certainly override this 
    on a production server that uses remote calendars.
    """
    
    user_model = "users.User"
    """Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
    `lino.modlib.users`"""
    
    projects_model = None
    """Optionally set this to the <applabel_modelname> of a 
    model used as project in your application."""
    
    
    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy database.    
    """
    
    migration_module = None
    """If you maintain a data migration module for your application, 
    specify its name here."""
    
    #~ bypass_perms = False
    
    use_gridfilters = True
    
    use_filterRow = not use_gridfilters
    """
    See :doc:`/blog/2011/0630`
    """
    
    use_awesome_uploader = False
    """
    Whether to use AwesomeUploader. 
    This feature was experimental and doesn't yet work (and maybe never will).
    """
    
    textfield_format = 'plain'
    """
    The default format for text fields. 
    Valid choices are currently 'plain' and 'html'.
    
    Text fields are either Django's `models.TextField` 
    or :class:`lino.fields.RichTextField`.
    
    You'll probably better leave the global option as 'plain', 
    and specify explicitly the fields you want as html by declaring 
    them::
    
      foo = fields.RichTextField(...,format='html')
    
    We even recommend that you declare your *plain* text fields also 
    using `fields.RichTextField` and not `models.TextField`::
    
      foo = fields.RichTextField()
    
    Because that gives subclasses of your application the possibility to 
    make that specific field html-formatted::
    
       resolve_field('Bar.foo').set_format('html')
       
    """
    
    use_tinymce = True
    """
    Whether to use TinyMCE instead of Ext.form.HtmlEditor. 
    See :doc:`/blog/2011/0523`
    """
    
    use_vinylfox = False
    """
    Whether to use VinylFox extensions for HtmlEditor. 
    This feature was experimental and doesn't yet work (and maybe never will).
    See :doc:`/blog/2011/0523`.
    """
    
    make_missing_dirs = True
    
    
    time_format_strftime = '%H:%M'
    time_format_extjs = 'H:i'
    
    date_format_strftime = '%d.%m.%Y'
    date_format_extjs = 'd.m.Y'
    
   
    def parse_date(self,s):
        """Convert a string formatted using 
        :attr:`date_format_strftime` or  :attr:`date_format_extjs` 
        into a datetime.date instance.
        See :doc:`/blog/2010/1130`.
        """
        ymd = reversed(map(int,s.split('.')))
        return datetime.date(*ymd)
        
    def parse_time(self,s):
        """Convert a string formatted using 
        :attr:`time_format_strftime` or  :attr:`time_format_extjs` 
        into a datetime.time instance.
        """
        hms = map(int,s.split(':'))
        return datetime.time(*hms)
        
    def parse_datetime(self,s):
        """Convert a string formatted for :meth:`parse_date` 
        and :meth:`parse_time` 
        into a datetime.datetime instance.
        """
        #~ print "20110701 parse_datetime(%r)" % s
        s2 = s.split()
        if len(s2) != 2:
            raise Exception("Invalid datetime value %r" % s)
        #~ ymd = map(int,s2[0].split('-'))
        #~ hms = map(int,s2[1].split(':'))
        #~ return datetime.datetime(*(ymd+hms))
        d = self.parse_date(s[0])
        t = self.parse_time(s[1])
        return datetime.combine(d,t)

    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    
    
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
    
    appy_params = dict(ooPort=8100)
    """
    Used by :class:`lino.mixins.printable.AppyBuildMethod`.
    """
    
    source_dir = os.path.dirname(__file__)
    source_name = os.path.split(source_dir)[-1]
    
    webdav_root = None
    """
    The path on server to store webdav files.
    Default is "PROJECT_DIR/media/webdav".
    """
    
    webdav_url = None
    """
    The URL prefix for webdav files.
    Default is "/media/webdav/".
    """
    
    loading_from_dump = False
    """
    Set to `False` by dpy dumps that were generated by
    :meth:`lino.utils.dpy.Serializer.serialize`.
    Used in 
    :func:`lino.modlib.cal.models.update_auto_task`
    and
    :mod:`lino.modlib.mails.models`.
    See also :doc:`/blog/2011/0901`.
    """
    
    def __init__(self,project_file,settings_dict):
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        self.qooxdoo_prefix = self.root_url + '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        self._setting_up = False
        self._setup_done = False
        #~ self._response = None
        self.settings_dict = settings_dict
        
        #~ self.appy_params.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\OPENOF~1.ORG\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/usr/bin/libreoffice')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')
    
        #~ if settings_dict: 
            #~ self.install_settings(settings_dict)
        if self.webdav_url is None:
            self.webdav_url = self.root_url + '/media/webdav/'
        if self.webdav_root is None:
            self.webdav_root = join(abspath(self.project_dir),'media','webdav')
            
        settings_dict.update(MEDIA_ROOT = join(self.project_dir,'media'))
        settings_dict.update(FIXTURE_DIRS = [join(self.project_dir,"fixtures")])
        settings_dict.update(TEMPLATE_DIRS = (
            join(abspath(self.project_dir),'templates'),
            join(abspath(self.source_dir),'templates'),
            join(abspath(dirname(__file__)),'templates'),
        ))
        
        try:
            from sitecustomize_lino import on_init
        except ImportError:
            pass
        else:
            on_init(self)
        
        #~ s.update(DATABASES= {
              #~ 'default': {
                  #~ 'ENGINE': 'django.db.backends.sqlite3',
                  #~ 'NAME': join(LINO.project_dir,'test.db')
              #~ }
            #~ })
        
        
        #~ self.source_name = os.path.split(self.source_dir)[-1]
        #~ # find the first base class that is defined in the Lino source tree
        #~ # this is to find out the source_name and the source_dir
        #~ for cl in self.__class__.__mro__:
            #~ if cl.__module__.startswith('lino.apps.'):
                #~ self.source_dir = os.path.dirname(__file__)
                #~ self.source_name = self.source_dir
                #~ os.path.split(_source_dir,
              
            
        # ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined.
        #~ from lino.models import get_site_config
        #~ self.config = get_site_config()
        
    #~ def get_user_model(self):
        #~ if 'django.contrib.auth' in self.settings_dict['INSTALLED_APPS']:
            #~ from django.contrib.auth.models import User
            #~ return 'auth.User'
        #~ else:
            #~ from lino.modlib.users.models import User
        #~ return User
        #~ return 'users.User'
      
        

    #~ def add_dummy_message(self,s):
        #~ self.dummy_messages.add(s)

    def setup_main_menu(self):
        pass

    #~ def update(self,**kw):
        #~ for k,v in kw.items():
            #~ assert self.hasattr(k)
            #~ setattr(self,k,v)
            
    #~ def update_settings(self,**kw):
        #~ self._settings_dict.update(kw)
            
    def configure(self,sc):
        self.config = sc
        
    def setup(self,**options):
        """
        This is called whenever a user interface 
        (:class:`lino.ui.base.UI`) gets instantiated (which usually 
        happenes in some URLConf, for example in:mod:`lino.ui.extjs3.urls`). 
        Also called by :term:`makedocs` with keyword argument `make_messages`.
        """
        from lino.core.kernel import setup_site
        setup_site(self,**options)


    def get_site_menu(self,ui,user):
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import menus
        main = menus.Toolbar('main')
        self.setup_menu(ui,user,main)
        url = self.root_url
        if not url: 
            url = "/"
        main.add_url_button(url,_("Home"))
        return main
        
    def setup_menu(self,ui,user,menu):
        raise NotImplementedError