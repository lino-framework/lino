# -*- coding: UTF-8 -*-
## Copyright 2002-2012 Luc Saffre
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
The ``lino`` module can be imported even from a Django :xfile:`settings.py` 
file since it does not import any django module.

"""

import os
import sys
import datetime
from os.path import join, abspath, dirname, normpath


__version__ = "1.4.1"
"""
Lino version number. 
*Released* versions are listed under :doc:`/releases`.
"""

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"

__copyright__ = """\
Copyright (c) 2002-2012 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""


gettext = lambda s: s

def language_choices(*args):
    """
    A subset of Django's LANGUAGES.
    See :doc:`/blog/2011/0226`.
    """
    _langs = dict(
        en=gettext('English'),
        de=gettext('German'),
        fr=gettext('French'),
        nl=gettext('Dutch'),
        et=gettext('Estonian'),
    )
    return [(x,_langs[x]) for x in args]
      



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

def using(ui=None):
    """
    Yields a list of third-party software descriptors used by Lino.
    Each descriptor is a tuple (name, version, url).
    
    """
    
    yield ("Lino",__version__,"http://lino.saffre-rumma.net")
    
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

    try:
        import reportlab
        version = reportlab.Version
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("ReportLab Toolkit",version,"http://www.reportlab.org/rl_toolkit.html")
               
    try:
        #~ import appy
        from appy import version
        version = version.verbose
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("appy.pod",version ,"http://appyframework.org/pod.html")
    
    import sys
    version = "%d.%d.%d" % sys.version_info[:3]
    yield ("Python",version,"http://www.python.org/")
    
    if ui is not None:
        #~ version = '<script type="text/javascript">document.write(Ext.version);</script>'
        onclick = "alert('ExtJS client version is ' + Ext.version);"
        tip = "Click to see ExtJS client version"
        text = "(version)"
        version = """<a href="#" onclick="%s" title="%s">%s</a>""" % (onclick,tip,text)
        yield ("ExtJS",version ,"http://www.sencha.com")


def welcome_text():
    #~ return "Lino version %s using %s" % (
    return "Using %s" % (', '.join(["%s %s" % (n,v) for n,v,u in using()]))

def welcome_html(ui=None):
    #~ return "Lino version %s using %s" % (
      #~ __version__,
      #~ ', '.join(['<a href="%s" target="_blank">%s</a> %s' % (u,n,v) for n,v,u in using(ui)]))
    sep = '<br/>'
    return sep.join(['<a href="%s" target="_blank">%s</a> %s' % (u,n,v) for n,v,u in using(ui)])


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
    """
    Path to the ExtJS root directory. 
    Only used on a development server if the `media` 
    directory has no symbolic link to the ExtJS root directory.
    """
    
    extensible_root = None
    """
    Path to the Extensible root directory. 
    Only used on a development server
    if the `media` directory has no symbolic link to the Extensible root directory
    and only if :attr:`use_extensible` is True.
    """
    
    tinymce_root = None
    """
    Path to the tinymce root directory. 
    Only to be used on a development server
    if the `media` directory has no symbolic link to the TinyMCE root directory
    and only if :attr:`use_tinymce` is True.
    """
    
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
    
    #~ person_model = None
    person_model = "contacts.Person"
    """
    If your application uses :model:`lino.modlib.contacts`,
    set this to a string "applabel.Modelname" which identifies 
    your Person model (which should inherit from
    :class:`lino.modlib.contacts.models.Person`).
    """
    
    #~ company_model = None
    company_model = "contacts.Company"
    """
    If your application uses :model:`lino.modlib.contacts`,
    set this to a string "applabel.Modelname" which identifies 
    your Company model (which should inherit from
    :class:`lino.modlib.contacts.models.Company`).
    """
    
    project_model = None
    """
    Optionally set this to the <applabel_modelname> of a 
    model used as project in your application.
    """
    
    user_model = "users.User"
    """Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
    `lino.modlib.users`. 
    
    Set it to `None` to remove any user management 
    (feature used by e.g. :mod:`lino.test_apps.1`)
    """
    
    default_user = None
    """
    Username to be used if a request with 
    no REMOTE_USER header makes its way through to Lino. 
    Which may happen on a development server and if Apache is 
    configured to allow it.
    Used by :mod:`lino.utils.auth`
    :mod:`lino.modlib.users.middleware`
    """
    
    remote_user_header = None
    
    #~ remote_user_header = "REMOTE_USER"
    """
    The name of the header (set by the web server) that Lino consults 
    for finding the user of a request.
    """
    #~ simulate_remote_user = False
    
    
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
    
    use_extensible = True
    """
    Whether to use the `Extensible <http://ext.ensible.com>`_ calendar library.
    """
    
    use_quicktips = False
    """
    Whether to make use of `Ext.QuickTips <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_.
    """
    
    use_css_tooltips = True
    """
    Whether to make use of `Ext.QuickTips <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_.
    """
    
    use_vinylfox = False
    """
    Whether to use VinylFox extensions for HtmlEditor. 
    This feature was experimental and doesn't yet work (and maybe never will).
    See :doc:`/blog/2011/0523`.
    """
    
    make_missing_dirs = True
    """
    Set this to False if you don't want Lino to automatically 
    create missing dirs when needed 
    (but to raise an exception in these cases, asking you to create it yourself)
    """
    
    
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
    
    source_dir = None # os.path.dirname(__file__)
    """
    Full path to the source directory of this Lino application.
    Local Lino subclasses should not override this variable.
    This is used e.g. in :mod:`lino.utils.config` to decide 
    whether there is a local config directory.
    """
    
    source_name = None  # os.path.split(source_dir)[-1]
    
    project_dir = None
    """
    Full path to your local project directory. 
    Local Lino subclasses should not override this variable.
    
    The local project directory is where 
    local configuration files are stored:
    
    - :xfile:`settings.py`, :xfile:`manage.py` and :xfile:`urls.py`
    - Your :xfile:`media` directory
    - Optional local :xfile:`config` and :xfile:`fixtures` directories
    """
    
    webdav_root = None
    """
    The path on server to store webdav files.
    Default is "PROJECT_DIR/media/webdav".
    """
    
    webdav_url = None
    """
    The URL prefix for webdav files.
    In a normal production configuration you should leave this to `None`, 
    Lino will set a default value "/media/webdav/",
    supposing that your Apache is configured as described in 
    :doc:`/admin/apache_webdav`.
    
    This may be used to simulate a :term:`WebDAV` location 
    on a development server.
    For example on a Windows machine, you may set it to ``w:\`` in your 
    :xfile:`sitecustomize_lino.py`::
    
        def on_init(LINO):
            (...)
            LINO.webdav_url = r"w:\"
      
    and before invoking :term:`runserver`, you issue in a command prompt::
    
        subst w: <dev_project_path>\media\webdav
        
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
    
    #~ decimal_separator = '.'
    decimal_separator = ','
    """
    Set this to either ``'.'`` or ``','`` to define wether to use 
    comma or dot as decimal separator when entering a `DecimalField`.
    """

    
    time_format_strftime = '%H:%M'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """
    
    time_format_extjs = 'H:i'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """
    
    date_format_strftime = '%d.%m.%Y'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    date_format_extjs = 'd.m.Y'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    """
    Alternative date entry formats accepted by Date widgets.
    """
    
    #~ date_format_regex = "/^[0123]\d\.[01]\d\.-?\d+$/"
    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    """
    Format (in Javascript regex syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    """
    Format (in strftime syntax) to use for formatting timestamps in AJAX responses.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    datetime_format_extjs = 'Y-m-d\TH:i:s'
    """
    Format (in ExtJS syntax) to use for formatting timestamps in AJAX calls.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    bcss_soap_url = None
    """
    URL of BCSS SOAP server
    """
    
    bcss_user_params = None
    u"""
    User parameters for BCSS access.
    
    Example::

      class Lino(Lino):
          ...
          bcss_user_params = dict(
                UserID='123', 
                Email='123@example.com', 
                OrgUnit='123', 
                MatrixID=12, 
                MatrixSubID=3)

    L’ « authorized user » est l’utilisateur de l’application. 
    Dans certains cas il s’agit de la personne physique derrière 
    la machine client, dans d’autres d’une application utilisant les services. 
    Ça correspond à un profil au niveau de la BCSS (cfr. IHFN et numéro de programme).
    
    « MatrixID » est l’identification dans la matrice, 
    c'est-à-dire, le secteur (17 pour les CPAS).
    
    « SubMatrixID » est l’identification du réseau 
    (0 pour primaire, 1 pour secondaire donc pour les CPAS...) 
    (voir « Service and Democlient usage »).
    
    « OrgUnit » est un identifiant pour l’organisme demandeur; 
    dans le cas des CPAS, le numéro KBO est utilisé.

    """
    
    use_davlink = False
    """
    Set this to `False` if you don't need WebDAV-enabled links.
    """
    
    languages = ['en']
    """
    A shortcut parameter to set the supported languages for this site.
    If specified, this must be an iterable of 2-letter codes.
    Examples::
    
      languages = "en de fr nl et".split()
      languages = ['en']
      
    The first language in this list will be the site's 
    default language.
      
    Lino will use it to set the Django 
    settings :setting:`LANGUAGES` and  :setting:`LANGUAGE_CODE`.
    The default value `None` means that Lino doesn't modify 
    these settings and that you are responsible for setting them 
    manually.
    
    """
    
    site_config_defaults = {}
    """
    Default values to be used when creating the persistent 
    :class:`lino.models.SiteConfig` instance.
    """
    
    index_view_action = 'lino.Home'
    
    # for internal use:
    _site_config = None
    
    
    def __init__(self,project_file,settings_dict):
      
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        
        self.source_dir = os.path.dirname(self.get_app_source_file())
        self.source_name = os.path.split(self.source_dir)[-1]
        
        #~ print "settings.LINO.source_dir:", self.source_dir
        #~ print "settings.LINO.source_name:", self.source_name

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
        
        settings_dict.update(
            MIDDLEWARE_CLASSES=tuple(
                self.get_middleware_classes()))

        self.startup_time = datetime.datetime.today()
        
        if self.languages:
            lc = language_choices(*self.languages)
            settings_dict.update(LANGUAGES = lc)
            settings_dict.update(LANGUAGE_CODE = lc[0][0])
        
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
        


    def parse_date(self,s):
        """Convert a string formatted using 
        :attr:`date_format_strftime` or  :attr:`date_format_extjs` 
        into a `(y,m,d)` tuple (not a `datetime.date` instance).
        See :doc:`/blog/2010/1130`.
        """
        ymd = tuple(reversed(map(int,s.split('.'))))
        assert len(ymd) == 3
        return ymd
        #~ return datetime.date(*ymd)
        
    def parse_time(self,s):
        """Convert a string formatted using 
        :attr:`time_format_strftime` or  :attr:`time_format_extjs` 
        into a datetime.time instance.
        """
        hms = map(int,s.split(':'))
        return datetime.time(*hms)
        
    def parse_datetime(self,s):
        """Convert a string formatted using
        :attr:`datetime_format_strftime` or  :attr:`datetime_format_extjs` 
        into a datetime.datetime instance.
        """
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = map(int,s2[0].split('-'))
        hms = map(int,s2[1].split(':'))
        return datetime.datetime(*(ymd+hms))
        #~ d = datetime.date(*self.parse_date(s[0]))
        #~ return datetime.combine(d,t)

    
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

    def get_app_source_file(self):
        "Override this in each application"
        return __file__
        
    def setup_main_menu(self):
        """
        To be implemented by applications.
        """
        pass

    #~ def update(self,**kw):
        #~ for k,v in kw.items():
            #~ assert self.hasattr(k)
            #~ setattr(self,k,v)
            
    #~ def update_settings(self,**kw):
        #~ self._settings_dict.update(kw)
            
    #~ def configure(self,sc):
        #~ self.config = sc
        
    def get_site_config(self):
        from lino.models import get_site_config
        return get_site_config()
        #~ if self._site_config is None:
            #~ from lino.models import get_site_config
            #~ self._site_config = get_site_config()
        #~ return self._site_config
    site_config = property(get_site_config)
        
        
    def setup(self,**options):
        """
        This is called whenever a user interface 
        (:class:`lino.ui.base.UI`) gets instantiated (which usually 
        happenes in some URLConf, for example in:mod:`lino.ui.extjs3.urls`). 
        #~ Also called by :term:`makedocs` with keyword argument `make_messages`.
        Also called by :term:`dtl2py` with keyword argument `make_messages`.
        """
        from lino.core.kernel import setup_site
        setup_site(self,**options)
        
        
    #~ def has_module(self,name):
        #~ from django.conf import settings
        #~ return name in settings.INSTALLED_APPS
        
    def is_installed(self,app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.
        """
        from django.conf import settings
        if not '.' in app_label:
            app_label = '.' + app_label
        for s in settings.INSTALLED_APPS:
            if s.endswith(app_label):
                return True

        


    def get_quicklinks(self,ui,user):
        from lino.utils import menus
        tb = menus.Toolbar('quicklinks')
        self.setup_quicklinks(ui,user,tb)
        return tb
        
    def get_site_menu(self,ui,user):
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import menus
        main = menus.Toolbar('main')
        self.setup_menu(ui,user,main)
        main.compress()
        url = self.root_url
        if not url: 
            url = "/"
        url = "javascript:Lino.close_all_windows()"
        main.add_url_button(url,label=_("Home"))
        
        if user:
            main.add_separator("->")
            main.add_instance_action(user)
        
        return main
        
    def setup_quicklinks(self,ui,user,tb):
        """Override this 
        in application-specific (or even local) :xfile:`settings.py` files 
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.apps.dsbe.settings.Lino.setup_quicklinks`.
        """
        pass
        
    def setup_menu(self,ui,user,menu):
        raise NotImplementedError
        
    #~ def get_calendar_color(self,calendar,request):
        #~ if calendar.user == request.user:
            #~ return 5
        #~ return 2
        
    def demo_date(self,days=0,**offset):
        if days:
            offset.update(days=days)
        #~ J = datetime.date(2011,12,16)
        if offset:
            return self.startup_time.date() + datetime.timedelta(**offset)
        return self.startup_time.date()
        
    def get_middleware_classes(self):
        """
        Yields the strings to be stored in 
        the :setting:`MIDDLEWARE_CLASSES` setting.
        
        In case you don't want to use this method
        for defining :setting:`MIDDLEWARE_CLASSES`, 
        you can simply set :setting:`MIDDLEWARE_CLASSES`
        in your :xfile:`settings.py` 
        after the :class:`lino.Lino` has been initialized.
        
        `Django and standard HTTP authentication
        <http://stackoverflow.com/questions/152248/can-i-use-http-basic-authentication-with-django>`_
        """

  
        yield 'django.middleware.common.CommonMiddleware'
        #~ yield 'django.contrib.sessions.middleware.SessionMiddleware'
        if self.languages and len(self.languages) > 1:
            yield 'django.middleware.locale.LocaleMiddleware'
        #~ yield 'django.contrib.auth.middleware.AuthenticationMiddleware'
        #~ if self.user_model:
        if self.remote_user_header:
            yield 'lino.utils.auth.RemoteUserMiddleware'
            yield 'django.middleware.doc.XViewMiddleware'
        else:
            yield 'lino.utils.auth.NoUserMiddleware'
        #~ yield 'lino.utils.editing.EditingMiddleware'
        yield 'lino.utils.ajax.AjaxExceptionResponse'


        if False: # not BYPASS_PERMS:
            yield 'django.contrib.auth.middleware.RemoteUserMiddleware'
            # TODO: find solution for this:
            #~ AUTHENTICATION_BACKENDS = (
              #~ 'django.contrib.auth.backends.RemoteUserBackend',
            #~ )
            
        if False:
            #~ yield 'lino.utils.sqllog.ShortSQLLogToConsoleMiddleware'
            yield 'lino.utils.sqllog.SQLLogToConsoleMiddleware'
            #~ yield 'lino.utils.sqllog.SQLLogMiddleware'
            
    def get_reminder_generators_by_user(self,user):
        """
        Override this per application to return a list of 
        reminder generators from all models for a give ueser
        A reminder generator is an object that has a `update_reminders` 
        method.
        """
        return []
        
