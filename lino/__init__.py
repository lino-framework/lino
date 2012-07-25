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


__version__ = "1.4.9"
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
        from odf import opendocument
        version = opendocument.__version__
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("OdfPy",version ,"http://pypi.python.org/pypi/odfpy")

    try:
        import docutils
        version = docutils.__version__
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("docutils",version ,"http://docutils.sourceforge.net/")

    try:
        import suds
        version = suds.__version__
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("suds",version ,"https://fedorahosted.org/suds/")

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
    
    if False:
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
        yield ("ReportLab",version,"http://www.reportlab.org/rl_toolkit.html")
               
    try:
        #~ import appy
        from appy import version
        version = version.verbose
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("Appy",version ,"http://appyframework.org/pod.html")
    
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
    return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in using()]))

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
    :mod:`lino.apps.pcsw.settings` or 
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
    
    never_build_site_cache = False
    """
    Set this to `True` if you want that Lino 
    never (re)builds the site cache (even when asked). 
    This can be useful on a development server when you are debugging 
    directly on the generated :xfile:`lino*.js`.
    Or for certain unit test cases.
    """
    
    build_js_cache_on_startup = None
    """
    Whether the Javascript cache files should be built on startup 
    for all user profiles and languages.
    
    On a production server this should be `True` for best performance,
    but while developing it is easier to set it to `False`, which means 
    that each file is built upon need (when a first request comes in).
    
    The default value `None` means that Lino decides automatically 
    (using :func:`lino.core.modeltools.is_devserver`).
    """
    
    # tree constants used by lino.modlib.workflows:
    max_state_value_length = 20 
    max_action_name_length = 50
    max_actor_name_length = 100
    
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
    
    #~ user_model = "users.User"
    user_model = None
    """
    Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
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
    Used by :mod:`lino.utils.auth`.
    """
    
    anonymous_user_profile = '900'
    
    
    
    remote_user_header = "REMOTE_USER"
    #~ remote_user_header = None
    """
    The name of the header (set by the web server) that Lino consults 
    for finding the user of a request.
    Default value is ``"REMOTE_USER"``.
    Settings this to `None` means that http authentication 
    is not used at all.
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
    
    use_quicktips = True
    """
    Whether to make use of `Ext.QuickTips
    <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_
    when displaying help texts defined in :class:`lino.models.HelpText`
    """
    
    use_css_tooltips = False
    """
    Whether to make use of CSS tooltips
    when displaying help texts defined in :class:`lino.models.HelpText`.
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
    Set to `False` by python dumps that were generated by
    :meth:`lino.utils.dumpy.Serializer.serialize`.
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
    comma or dot as decimal point separator when entering 
    a `DecimalField`.
    """
    
    #~ decimal_group_separator = ','
    decimal_group_separator = ' '
    """
    Decimal group separator for :func:`lino.utils.moneyfmt`.
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
    Alternative date entry formats accepted by ExtJS Date widgets.
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
    
    cbss_live_tests = False
    """
    Whether unit tests should try to really connect to the cbss.
    Some test cases of the test suite would fail with a timeout if run 
    from behind an IP address that is not registered at the :term:`CBSS`.
    These tests are skipped by default. To activate them, 
    set `cbss_live_tests` to `True` in your :xfile:`settings.py`.
    
    """
    
    unused_cbss_user_params = None
    u"""
    User parameters for CBSS SSDN (classic) services.
    
    Example::

      class Lino(Lino):
          ...
          cbss_user_params = dict(
                UserID='123', 
                Email='123@example.com', 
                OrgUnit='123', 
                MatrixID=17, 
                MatrixSubID=1)

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
    
    cbss_environment = None
    """
    Either `None` or one of 'test', 'acpt' or 'prod'.
    See :mod:`lino.modlib.cbss.models`.
    Leaving this to `None` means that the cbss module is "inactive" even if installed.
    """
    
    unused_cbss_cbe_number = '0123456789'
    """
    Either `None` or a string of style '0123456789'
    Needed for CBSS new style services. See :mod:`lino.modlib.cbss.models`.
    """
    unused_cbss_username = None
    """
    Either `None` or a string of style 'E0123456789'
    Needed for CBSS new style services. See :mod:`lino.modlib.cbss.models`.
    """
    unused_cbss_password = None
    """
    Either `None` or a string of style 'p1234567890abcd1234567890abcd'
    Needed for CBSS new style services. See :mod:`lino.modlib.cbss.models`.
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
    
    max_auto_events = 36
    """
    Maximum number of automatic events to be generated 
    by :class:`lino.modlib.cal.models.EventOwner`.
    """
    
    #~ use_contenttypes = True
    #~ """
    #~ Set this to False if you don't want to use `django.contrib.contenttypes`.
    #~ """
    
    #~ index_view_action = 'lino.Home'
    
    
    
    
    # for internal use:
    
    _site_config = None
    _extjs_ui = None
    _groph_ui = None
    
    
    def __init__(self,project_file,settings_dict):
      
        #~ self.user_profile_fields = ['level']
        
        #~ self.version = __version__
        
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
        if self.project_dir != self.source_dir:
            settings_dict.update(FIXTURE_DIRS = [join(self.project_dir,"fixtures")])
            #~ lino.Lino.__init__ füllte project_dir auch dann nach FIXTURES_DIR, 
            #~ wenn es zugleich das source_dir war. Was die subtile Folge hatte, 
            #~ dass alle Fixtures doppelt ausgeführt wurden. 
            #~ Dieser Bug hat mich mindestens eine Stunde lang beschäftigt.            

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
        

    def get_ui(self):
        if self._extjs_ui is None:
            self.startup()
            from lino.ui.extjs3 import UI
            self._extjs_ui = UI()
        return self._extjs_ui
    ui = property(get_ui)

    def get_groph_ui(self):
        if self._groph_ui is None:
            self.startup()
            from lino.ui.groph.groph_ui import UI
            self._groph_ui = UI()
        return self._groph_ui
    groph_ui = property(get_groph_ui)

    override_modlib_models = []
    """
    A list of names of modlib models which are being 
    redefined by this application.
    
    The following modlib models currently support this:
    - :class:`contacts.Person <lino.modlib.contacts.models.Person>`
    - :class:`contacts.Company <lino.modlib.contacts.models.Company>`
    
    Usage: in your application's `settings.py`, specify::
    
      class Lino(Lino):
          override_modlib_models = ['contacts.Person']
          
    This will cause the modlib Person model to be abstract, 
    and hence your application is responsible for defining another 
    `Person` class with "contacts" as `app_label`::
          
      class Person(contacts.Person,contacts.Born):
          class Meta(contacts.Person.Meta):
              app_label = 'contacts'
              
          def kiss(self):
              ...
          
    
    """
    
    def site_header(self):
        """
        Used e.g. in footnote or header of certain printed documents.
        """
        if self.is_installed('contacts'):
            if self.site_config.site_company:
                return self.site_config.site_company.address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return s

    def site_version(self):
        """
        Used e.g. in footnote or header of certain printed documents.
        """
        return "Lino " + __version__

    def is_abstract_model(self,name):
        return name in self.override_modlib_models
        
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
        
    def on_site_config_saved(self,sc):
        """
        Used internally. Called by SiteConfig.save() to update the cached instance.
        """
        self._site_config = sc
        
    def get_site_config(self):
        """
        Returns the one and only :class:`lino.models.SiteConfig` instance.
        
        If no instance exists (which happens in a virgin database),
        we create it and set some default values from :attr:`site_config_defaults`.
        """
        if self._site_config is None:
            from lino.models import SiteConfig
            try:
                self._site_config = SiteConfig.objects.get(pk=1)
            except SiteConfig.DoesNotExist:
            #~ except Exception,e:
                kw = dict(pk=1)
                #~ kw.update(settings.LINO.site_config_defaults)
                kw.update(self.site_config_defaults)
                #~ logger.debug("Creating SiteConfig record (%s)",e)
                self._site_config = SiteConfig(**kw)
                # 20120725 
                # tutorials.t1 menu selection `Config --> Site Parameters` 
                # said "SiteConfig 1 does not exist"
                # don't remember why we wanted to NOT save the instance here 
                self._site_config.save()
        return self._site_config
    site_config = property(get_site_config)
    
    def update_site_config(self,**kw):
        """
        Update and save the one and only :class:`lino.models.SiteConfig` instance.
        """
        sc = self.site_config
        for k,v in kw.items():
            setattr(sc,k,v)
        sc.save()
    
        
    def startup(self,**options):
        """
        Start the Lino site. 
        This is called when Django has done his work 
        (all models modules have been imported).
        
        This is called whenever a user interface 
        (:class:`lino.ui.base.UI`) gets instantiated (which usually 
        happenes in some URLConf, for example in:mod:`lino.ui.extjs3.urls`). 
        Also called by some test cases.
        """
        from lino.core.kernel import startup_site
        startup_site(self,**options)
        #~ print "20120725 save site config"
        #~ self.site_config.save()
        
        
    #~ def has_module(self,name):
        #~ from django.conf import settings
        #~ return name in settings.INSTALLED_APPS
        
    #~ def add_user_group(self,name,label):
        #~ from lino.utils.choicelists import UserLevel, UserGroup
        #~ UserGroup.add_item(name,label,name)
        #~ self.add_user_field(name+'_level',UserLevel.field(label),profile=True)
        
    def setup_choicelists(self):
        """
        Redefine application-specific Choice Lists.
        
        Especially used to define application-specific
        :class:`UserProfiles <lino.core.perms.UserProfiles>`.
        
        Lino by default has two user profiles "User" 
        and "Administrator", defined in :mod:`lino.core.perms`.
        
        Application developers who use group-based requirements 
        must override this in their application's :xfile:`settings.py` 
        to provide a default list of user profiles for their 
        application.
        
        See the source code of :mod:`lino.apps.presto` 
        or :mod:`lino.apps.pcsw` for a usage example.
        
        Local site administrators may again override this in their 
        :xfile:`settings.py`.
        
        """
        pass
        
    def add_user_field(self,name,fld):
        if self.user_model:
            from lino import dd
            User = dd.resolve_model(self.user_model)            
            dd.inject_field(User,name,fld)
            #~ if profile:
                #~ self.user_profile_fields.append(name)

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
        #~ print "20120703 not installed: %r" % app_label

        
    def get_quicklinks(self,ui,user):
        from lino.core import menus
        tb = menus.Toolbar(user,'quicklinks')
        self.setup_quicklinks(ui,user,tb)
        return tb
        
    def get_site_menu(self,ui,user):
        from django.utils.translation import ugettext_lazy as _
        from lino.core import menus
        main = menus.Toolbar(user,'main')
        self.setup_menu(ui,user,main)
        main.compress()
        url = self.root_url
        if not url: 
            url = "/"
        url = "javascript:Lino.close_all_windows()"
        main.add_url_button(url,label=_("Home"))
        
        #~ 20120626 if self.user_model:
            #~ from lino.modlib.users import models as users
            #~ main.add_separator("->")
            #~ main.add_instance_action(user)
            #~ main.add_action(users.MyDetail)
            #~ main.add_action(users.Users.detail_action)
        
        return main
        
    def setup_quicklinks(self,ui,user,m):
        """
        Override this 
        in application-specific (or even local) :xfile:`settings.py` files 
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.apps.pcsw.settings.Lino.setup_quicklinks`.
        """
        self.on_each_app('setup_quicklinks',ui,user,m)
        
    def setup_menu(self,ui,user,main):
        """
        Set up the application's menu structure.
        
        The default implementation use a system of 
        predefined top-level items that are filled by the 
        different :setting:`INSTALLED_APPS`.
        
        Deserves more documentation.
        
        """
        from django.utils.translation import ugettext_lazy as _
        m = main.add_menu("master",_("Master"))
        self.on_each_app('setup_master_menu',ui,user,m)
        if not user.profile.readonly:
            m = main.add_menu("my",_("My menu"))
            self.on_each_app('setup_my_menu',ui,user,m)
        self.on_each_app('setup_main_menu',ui,user,main)
        m = main.add_menu("config",_("Configure"))
        self.on_each_app('setup_config_menu',ui,user,m)
        m = main.add_menu("explorer",_("Explorer"))
        self.on_each_app('setup_explorer_menu',ui,user,m)
        m = main.add_menu("site",_("Site"))
        self.on_each_app('setup_site_menu',ui,user,m)
        return main


    def on_each_app(self,methname,*args):
        """
        Call the named method on each module in :setting:`INSTALLED_APPS`
        that defines it.
        """
        from django.conf import settings
        from django.utils.importlib import import_module
        from lino.utils import dblogger
        
        for app_name in settings.INSTALLED_APPS:
            mod = import_module('.models', app_name)
            meth = getattr(mod,methname,None)
            if meth is not None:
                dblogger.debug("Running %s of %s", methname, mod.__name__)
                meth(self,*args)
        
        
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
        #~ if self.user_model is None:
            #~ yield 'lino.utils.auth.NoUserMiddleware'
        #~ elif self.remote_user_header:
        if self.remote_user_header:
            yield 'lino.utils.auth.RemoteUserMiddleware'
            #~ yield 'django.middleware.doc.XViewMiddleware'
        else:
            raise Exception("""\
`user_model` is not None, but no `remote_user_header` in your settings.LINO.""")
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
            
    def get_main_action(self,user):
        """
        Return the action to show as top-level "index.html"
        """
        return None
        #~ return self.modules.lino.Home.default_action
        
    def get_main_html(self,request):
        """
        Return a chunk of html to be displayed in the main area.
        This is visible only if :meth:`get_main_action` returns `None`.
        """
        return None


    def get_reminder_generators_by_user(self,user):
        """
        Override this per application to return a list of 
        reminder generators from all models for a give ueser
        A reminder generator is an object that has a `update_reminders` 
        method.
        """
        return []
        
    def install_migrations(self,globals_dict):
        """
        Called from python dumps.
        New in version 1.4.4. (replaces the previous migrations_module) 
        """
        #~ import logging
        #~ dblogger = logging.getLogger(__name__)
        from lino.utils import dblogger
        from django.utils.importlib import import_module
        if globals_dict['SOURCE_VERSION'] == __version__:
            dblogger.info("Source version is %s : no migration needed", __version__)
            return
        if self.migration_module:
            migmod = import_module(self.migration_module)
        else:
            migmod = self
        while True:
            from_version = globals_dict['SOURCE_VERSION']
            funcname = 'migrate_from_' + from_version.replace('.','_')
            m = getattr(migmod,funcname,None)
            #~ func = globals().get(funcname,None)
            if m:
                #~ dblogger.info("Found %s()", funcname)
                to_version = m(globals_dict)
                if not isinstance(to_version,basestring):
                    raise Exception("Oops: %s didn't return a string!" % m)
                msg = "Migrating from version %s to %s" % (from_version, to_version)
                if m.__doc__:
                    msg += ":\n" + m.__doc__
                dblogger.info(msg)
                globals_dict['SOURCE_VERSION'] = to_version
            else:
                if from_version != __version__:
                    dblogger.warning("No method for migrating from version %s to %s",from_version,__version__)
                break

          
