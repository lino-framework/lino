# -*- coding: UTF-8 -*-
## Copyright 2002-2013 Luc Saffre
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
import cgi
import inspect
import datetime

from os.path import join, abspath, dirname, normpath, isdir
from decimal import Decimal
from urllib import urlencode

def buildurl(*args,**kw):
    url = '/' + ("/".join(args))
    if len(kw):
        url += "?" + urlencode(kw)
    return url
        


from lino.utils.xmlgen import html as xghtml

__version__ = "1.5.5"
"""
Lino version number. 
"""

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
__url__ = "http://www.lino-framework.org"


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
    but while developing, it may be easier to set it to `False`, which means 
    that each file is built upon need (when a first request comes in).
    
    The default value `None` means that Lino decides automatically 
    in :func:`lino.core.kernel.startup_site`: 
    if becomes `False` if
    either :func:`lino.core.modeltools.is_devserver` returns True
    or setting:`DEBUG` is set.
    """
    
    # three constants used by lino.modlib.workflows:
    max_state_value_length = 20 
    max_action_name_length = 50
    max_actor_name_length = 100
    
    use_experimental_features = False
    """
    Whether to include "experimental" features.
    """
    
    use_spinner = False # doesn't work. leave this to False
    
    plain_prefix = '/plain' 
    
    admin_prefix = '' 
    #~ admin_url = 'admin/'
    #~ admin_prefix = '/admin'
    #~ admin_url = '' # 
    """
    The prefix to use for Lino admin URLs.
    
    The default value is an empty string, resulting in a 
    website whose root url shows the "admin mode" 
    (i.e. with a pull-down "main menu").
    
    Note that unlike Django's `MEDIA_URL
    <https://docs.djangoproject.com/en/dev/ref/settings/#media-url>`__ 
    setting, this must **begin** and **not end** with a slash if set 
    to a non-empty value.
    
    If this is nonempty, then your site features a "web content mode": 
    the root url renders "web content" defined by :mod:`lino.modlib.pages`.
    The usual value in that case is ``admin_prefix = "/admin"``.
    
    
    See also  
    http://groups.google.com/group/django-users/browse_thread/thread/c95ba83e8f666ae5?pli=1
    http://groups.google.com/group/django-users/browse_thread/thread/27f035aa8e566af6
    https://code.djangoproject.com/ticket/8906
    https://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#ChangedthewayURLpathsaredetermined
    """
    
    
    extjs_root = None
    """
    Path to the ExtJS root directory. 
    Only used on a development server if the `media` 
    directory has no symbolic link to the ExtJS root directory.
    """
    
    bootstrap_root = None
    """
    Path to the Jasmine root directory. 
    Only used on a development server
    whose `media` directory hasn't already a symbolic link or subdirectory,
    and only if :attr:`use_bootstrap` is True.
    """
    
    jasmine_root = None
    """
    Path to the Jasmine root directory. 
    Only used on a development server
    if the `media` directory has no symbolic link to the Jasmine root directory
    and only if :attr:`use_jasmine` is True.
    """
    
    extensible_root = None
    """
    Path to the Extensible root directory. 
    Only used on a development server
    if the `media` directory has no symbolic link to the Extensible root directory,
    and only if :attr:`use_extensible` is True.
    """
    
    tinymce_root = None
    """
    Path to the tinymce root directory. 
    Only to be used on a development server
    if the `media` directory has no symbolic link to the TinyMCE root directory,
    and only if :attr:`use_tinymce` is True.
    """
    
    eid_jslib_root = None
    """
    Path to the `eid_jslib` root directory. 
    Only to be used on a development server
    if the `media` directory has no symbolic link to the directory,
    and only if :attr:`use_eid_jslib` is True.
    http://code.google.com/p/eid-javascript-lib/
    """
    
    
    
    allow_duplicate_cities = False
    """Set this to True if that's what you want. 
    In normal situations you shouldn't, but one exception is here :doc:`/blog/2011/0830`
    """
    
    
    help_url = "http://code.google.com/p/lino"
    #~ site_url = 
    #~ index_html = "This is the main page."
    title = None
    #~ domain = "www.example.com"
    
    pypi_name = None
    """
    The PyPI name of this application. 
    Used in :xfile:`setup.py` file as the `name` argument to 
    `setuptools.setup() <http://guide.python-distribute.org/creation.html>`_.
    """
    
    short_name = None # "Unnamed Lino Application"
    """
    Used as display name to end-users at different places.
    """
    
    author = None
    author_email = None
    version = None
    """
    """
    
    url = None
    """
    """
    
    description = """yet another <a href="%s">Lino</a> application.""" % __url__
    """
    A short single-sentence description.
    It should start with a lowercase letter because the beginning 
    of the sentence will be generated from other class attributes 
    like :attr:`short_name` and :attr:`version`.
    """
    
    #~ def get_application_description(self):
        #~ info = self.get_application_info()
        #~ s = """%s is yet another 
        #~ <a href="%s">Lino</a> application.
        #~ """ % (info[0],__url__)
        #~ if False:
            #~ from django.db import models
            #~ s += """
            #~ It features %d database tables in %d modules.
            #~ """ % (len(list(models.get_models())),len(list(self.get_installed_apps())))
        #~ return s
    
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
    
    anonymous_user_profile = '000'
    """
    The UserProfile (or rather it's value) to assigned to anonymous user.
    
    """
    
    
    
    #~ remote_user_header = "REMOTE_USER"
    remote_user_header = None
    """
    The name of the header (set by the web server) that Lino consults 
    for finding the user of a request.
    The default value `None` means that http authentication is not used.
    Apache's default value is ``"REMOTE_USER"``.
    """
    
    #~ simulate_remote_user = False
    
    
    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy database.    
    """
    
    migration_module = None
    """If you maintain a data migration module for your application, 
    specify its name here."""
   
    use_gridfilters = True
    
    use_eid_applet = False
    """
    Whether to include functionality to read Belgian id cards
    using the official 
    `eid-applet <http://code.google.com/p/eid-applet>`_.
    This option is experimental and doesn't yet work.
    See :doc:`/blog/2012/1105`.
    """
    
    use_eid_jslib = False
    """
    Whether to include functionality to read Belgian id cards    
    using Johan De Schutter's
    `eid-javascript-lib <http://code.google.com/p/eid-javascript-lib/>`_.
    
    If this is True, Lino expects eid-javascript-lib
    to be installed in a directory `media/beid-jslib`.
    See also :attr:`eid_jslib_root`.
    
    """
    
    use_esteid = False
    """
    Whether to include functionality to read Estonian id cards.
    This option is experimental and doesn't yet work.
    """
    
    
    use_filterRow = not use_gridfilters
    """
    See :doc:`/blog/2011/0630`.
    This option was experimental and doesn't yet work (and maybe never will).
    """
    
    use_awesome_uploader = False
    """
    Whether to use AwesomeUploader. 
    This option was experimental and doesn't yet work (and maybe never will).
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
    See also :attr:`tinymce_root`.
    See :doc:`/blog/2011/0523`.
    """
    
    use_bootstrap = True
    """
    Whether to use the `Bootstrap  <http://twitter.github.com/bootstrap>`_ CSS toolkit.
    """
    
    use_jasmine = False
    """
    Whether to use the `Jasmine <https://github.com/pivotal/jasmine>`_ testing library.
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
    
    catch_layout_exceptions = True
    """
    Lino usually catches any exception during 
    :meth:`lino.ui.extjs3.ExtUI.create_layout_element`
    to report errors of style 
    "Unknown element "postings.PostingsByController ('postings')" 
    referred in layout <PageDetail on pages.Pages>."
    
    Setting this to `False` is
    useful when there's some problem *within* the framework.
    
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
    
    #~ source_dir = None # os.path.dirname(__file__)
    #~ """
    #~ Full path to the source directory of this Lino application.
    #~ Local Lino subclasses should not override this variable.
    #~ This is used in :mod:`lino.utils.config` to decide 
    #~ whether there is a local config directory.
    #~ """
    
    #~ source_name = None  # os.path.split(source_dir)[-1]
    
    project_name = None
    """
    Read-only.
    The leaf name of your local project directory.
    """
    
    project_dir = None
    """
    Read-only.
    Full path to your local project directory. 
    Local Lino subclasses should not override this variable.
    
    The local project directory is where 
    local configuration files are stored:
    
    - Your :xfile:`settings.py`
    - Optionally the :xfile:`manage.py` and :xfile:`urls.py` files
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
    For example on a Windows machine, you may set it to ``w:\``,      
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
    
    uppercase_last_name = False
    """
    Whether last name of persons should be printed with uppercase letters.
    See :mod:`lino.test_apps.human`
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
    
    #~ def override_user_language(self):
        #~ """
        #~ Called for each request. If this returns a non-empty string, 
        #~ it overrides the value of user's language field.
        #~ """
        #~ return None
    
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
          
      class Person(contacts.Person,mixins.Born):
          class Meta(contacts.Person.Meta):
              app_label = 'contacts'
              
          def kiss(self):
              ...
    
    """
    
    modules = None
    """
    A shortcut to access all installed models and actors.
    Read-only. Applications should not set this. 
    """
    
    django_settings = None
    """
    This is where Lino stores the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when 
    calling :meth:`Lino.__init__`.
    """
    
    
    demo_fixtures = ['std','demo']
    """
    The list of fixtures to be loaded by the 
    `initdb_demo <lino.management.commands.initdb_demo>`
    command.
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
    
    
    def __init__(self,project_file,django_settings):
      
        #~ self.user_profile_fields = ['level']
        
        #~ self.version = __version__
        
        #~ self._watch_changes_requests = []
        
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        
        
        self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        self._setting_up = False
        self._setup_done = False
        #~ self._response = None
        self.django_settings = django_settings
        
        
        installed_apps = tuple(self.get_installed_apps())
        django_settings.update(INSTALLED_APPS=installed_apps)
        
        """
        The `is_local_project_dir` flag contains `True` if this is a "local" project.
        A project is called local if 
        """
        self.is_local_project_dir = self.__module__ in installed_apps
        #~ self.is_app = os.path.exist(join(self.project_dir,'models.py'))
        
        #~ self.source_dir = os.path.dirname(self.get_app_source_file())
        #~ self.source_name = os.path.split(self.source_dir)[-1]
        
        #~ print "settings.LINO.source_dir:", self.source_dir
        #~ print "settings.LINO.source_name:", self.source_name

        #~ self.appy_params.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\OPENOF~1.ORG\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/usr/bin/libreoffice')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')
    
        #~ if django_settings: 
            #~ self.install_settings(django_settings)
        if self.webdav_url is None:
            self.webdav_url = '/media/webdav/'
        if self.webdav_root is None:
            self.webdav_root = join(abspath(self.project_dir),'media','webdav')
            
        django_settings.update(MEDIA_ROOT = join(self.project_dir,'media'))
        
        """
        If your project_dir contains no :xfile:`models.py`, 
        but *does* contain a `fixtures` subdir, 
        then Lino automatically adds this as "local fixtures directory" 
        to Django's `FIXTURE_DIRS`.
        """
        if self.is_local_project_dir:
            pth = join(self.project_dir,'fixtures')
            if isdir(pth):
                django_settings.update(FIXTURE_DIRS = [pth])
                
        #~ get_settings_subdirs
            
        #~ if self.project_dir != self.source_dir:
            #~ django_settings.update(FIXTURE_DIRS = [join(self.project_dir,"fixtures")])
            #~ lino.Lino.__init__ füllte project_dir auch dann nach FIXTURES_DIR, 
            #~ wenn es zugleich das source_dir war. Was die subtile Folge hatte, 
            #~ dass alle Fixtures doppelt ausgeführt wurden. 
            #~ Dieser Bug hat mich mindestens eine Stunde lang beschäftigt.            

        #~ django_settings.update(TEMPLATE_DIRS = (
            #~ join(abspath(self.project_dir),'templates'),
            #~ join(abspath(self.source_dir),'templates'),
            #~ join(abspath(dirname(__file__)),'templates'),
        #~ ))
        
        django_settings.update(
            MIDDLEWARE_CLASSES=tuple(
                self.get_middleware_classes()))
                
        django_settings.update(
            TEMPLATE_LOADERS=tuple(
                ['lino.core.web.Loader']
                ))


        self.startup_time = datetime.datetime.now()
        
        if self.languages:
            lc = language_choices(*self.languages)
            django_settings.update(LANGUAGES = lc)
            django_settings.update(LANGUAGE_CODE = lc[0][0])
        
        try:
            from lino_local import on_init
            #~ from sitecustomize_lino import on_init
            #~ import sitecustomize_lino
            #~ raise Exception("""
            #~ Replace your sitecustomize_lino module 
            #~ (%s)
            #~ by a LocalLinoMixin
            #~ as documented in 
            #~ http://lino-framework.org/admin/local_lino.html
            #~ """ % sitecustomize_lino.__file__)
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
        
    def get_settings_subdirs(self,subdir_name):
        """
        Yield all (existing) directories named `subdir_name` 
        of this site's project directory and it's inherited 
        project directories.
        """
        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)),subdir_name)
                if isdir(pth):
                    yield pth
          
       
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

    def site_header(self):
        """
        Used e.g. in footnote or header of certain printed documents.
        """
        if self.is_installed('contacts'):
            if self.site_config.site_company:
                return self.site_config.site_company.address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return s

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
        #~ if 'django.contrib.auth' in self.django_settings['INSTALLED_APPS']:
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

        
    def get_site_config(self):
        """
        Returns the one and only :class:`lino.models.SiteConfig` instance.
        
        If no instance exists (which happens in a virgin database),
        we create it and set some default values from :attr:`site_config_defaults`.
        """
        if self._site_config is None:
            #~ print '20120801 create _site_config'
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
    
    def on_site_config_saved(self,sc):
        """
        Used internally. Called by SiteConfig.save() to update the cached instance.
        """
        self._site_config = sc
        #~ print '20120801 site_conf saved', sc.propgroup_softskills
        
    def update_site_config(self,**kw):
        """
        Update and save the one and only :class:`lino.models.SiteConfig` instance.
        """
        #~ print '20120801 update_site_config', kw
        sc = self.site_config
        for k,v in kw.items():
            setattr(sc,k,v)
        sc.save()
        #~ self.on_site_config_saved(sc)
    
    def is_imported_partner(self,obj):
        """
        Return whether the specified
        :class:`Partner <lino.modlib.contacts.models.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
                  
        
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
        
        
    def setup_workflows(self):
        self.on_each_app('setup_workflows')
        
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
        
        Note that you may not specify values longer 
        than `max_length` when redefining your choicelists.
        This limitation is because these redefinitions happen at a 
        moment where database fields have already been instantiated, 
        so it is too late to change their max_length.        
        Not that this limitation is only for the *values*, not for the names 
        or texts of choices.
        
        """
        
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset()
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"), name='anonymous', level=None,
            #~ readonly=True,
            authenticated=False)
        add('100', _("User"), name='user', level='user')
        add('900', _("Administrator"), name='admin', level='admin')
        
        
        
    def add_user_field(self,name,fld):
        if self.user_model:
            from lino import dd
            #~ User = dd.resolve_model(self.user_model)            
            dd.inject_field(self.user_model,name,fld)
            #~ if profile:
                #~ self.user_profile_fields.append(name)

    def is_installed(self,app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.
        """
        from django.conf import settings
        #~ if not '.' in app_label:
            #~ app_label = '.' + app_label
        for s in settings.INSTALLED_APPS:
            if s == app_label or s.endswith('.'+app_label):
            #~ if s.endswith(app_label):
                return True
        #~ print "20120703 not installed: %r" % app_label

        
    def get_quicklinks(self,ar):
        from lino.core import menus
        m = menus.Toolbar(ar.get_user().profile,'quicklinks')
        self.setup_quicklinks(ar,m)
        return m
        
    def get_site_menu(self,ui,profile):
        """
        Return this site's main menu for the given user. 
        Must be a :class:`lino.core.menus.Toolbar` instance.
        Applications usually should not need to override this.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino.core import menus
        main = menus.Toolbar(profile,'main')
        self.setup_menu(ui,profile,main)
        main.compress()
        #~ url = self.admin_url
        #~ if not url: 
            #~ url = "/"
        #~ url = "javascript:Lino.close_all_windows()"
        #~ main.add_url_button(url,label=_("Home"))
        main.add_item('home',_("Home"),javascript="Lino.close_all_windows()")
        
        return main
        
    def setup_quicklinks(self,ar,m):
        """
        Override this 
        in application-specific (or even local) :xfile:`settings.py` files 
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.apps.pcsw.settings.Lino.setup_quicklinks`.
        """
        self.on_each_app('setup_quicklinks',ar,m)
        
    def setup_menu(self,ui,profile,main):
        """
        Set up the application's menu structure.
        
        The default implementation uses a system of 
        predefined top-level items that are filled by the 
        different :setting:`INSTALLED_APPS`.
        To use this system, application programmers 
        define one or several of the following functions in 
        their `modules` module:
        
        - `setup_master_menu`
        - `setup_main_menu`
        - `setup_reports_menu`
        - `setup_config_menu`
        - `setup_explorer_menu`
        - `setup_site_menu`
        
        These functions, if present, will be called with three 
        positional arguments: `ui`, `profile` and `menu`.
        
        Deserves more documentation.
        
        """
        from django.utils.translation import ugettext_lazy as _
        m = main.add_menu("master",_("Master"))
        self.on_each_app('setup_master_menu',ui,profile,m)
        #~ if not profile.readonly:
            #~ m = main.add_menu("my",_("My menu"))
            #~ self.on_each_app('setup_my_menu',ui,profile,m)
        self.on_each_app('setup_main_menu',ui,profile,main)
        m = main.add_menu("reports",_("Reports"))
        self.on_each_app('setup_reports_menu',ui,profile,m)
        m = main.add_menu("config",_("Configure"))
        self.on_each_app('setup_config_menu',ui,profile,m)
        m = main.add_menu("explorer",_("Explorer"))
        self.on_each_app('setup_explorer_menu',ui,profile,m)
        m = main.add_menu("site",_("Site"))
        self.on_each_app('setup_site_menu',ui,profile,m)
        return main


    def get_installed_modules(self):
        from django.conf import settings
        from django.utils.importlib import import_module
        for app_name in settings.INSTALLED_APPS:
            yield import_module('.models', app_name)
        
    def on_each_app(self,methname,*args):
        """
        Call the named method on each module in :setting:`INSTALLED_APPS`
        that defines it.
        """
        from lino.utils import dblogger
        for mod in self.get_installed_modules():
            meth = getattr(mod,methname,None)
            if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
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
        if self.user_model is None:
            yield 'lino.utils.auth.NoUserMiddleware'
        else:
            if self.remote_user_header:
                yield 'lino.utils.auth.RemoteUserMiddleware'
                #~ yield 'django.middleware.doc.XViewMiddleware'
            else:
                # 20121003 : not using remote http auth, so we need sessions
                yield 'django.contrib.sessions.middleware.SessionMiddleware'
                yield 'lino.utils.auth.SessionUserMiddleware'
                #~ raise Exception("""\
    #~ `user_model` is not None, but no `remote_user_header` in your settings.LINO.""")
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
            
    def get_main_action(self,profile):
        """
        Return the action to show as top-level "index.html".
        The default implementation returns `None`, which means 
        that Lino will call :meth:`get_main_html`.
        """
        return None
        
    
    #~ MAIN_HTML_TEMPLATE = Template("""\
    #~ <div class="htmlText">
    #~ <h1>{{node.title}}</h1>
    #~ {{parse(node.body)}}
    #~ </div>""")

        
        
    def get_main_html(self,request):
        """
        Return a chunk of html to be displayed in the main area of the admin index.
        This is being called only if :meth:`get_main_action` returns `None`.
        The default implementation returns the message 
        "You are now in the admin section..."
        """
        from lino.core import web
        return web.render_from_request(request,'admin_main.html')
        
    def unused_get_main_html(self,request):
        """
        Return a chunk of html to be displayed in the main area of the admin index.
        This is being called only if :meth:`get_main_action` returns `None`.
        The default implementation returns the 
        message "It works! But your application isn't complete. ..."
        """
        pages = dd.resolve_app('pages')
        from lino.utils import babel
        node = pages.lookup('admin')
        if node is None:
            return '20121221 No admin page within %s' % [cgi.escape(unicode(p)) for p in pages.get_all_pages()]
        return pages.render_node(request,node,'admin_main.html')


    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    """
    
    def get_vat_class(self,tt,item):
        return 'normal'
        
    def get_product_vat_class(self,tt,product):
        return 'normal'
        

    def get_product_base_account(self,tt,product):
        """
        Return the reference of the general account 
        to be used to book the product movement of 
        the trade type and product.
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        if tt.name == 'sales':
            #~ return '7000'
            return 'sales'
        elif tt.name == 'purchases':
        #~ elif item.voucher.journal.type == JournalTypes.purchases:
            return 'purchases'
            #~ return '6000'
        
    #~ def get_sales_item_account(self,item):
        #~ return self.modules.accounts.Account.objects.get(group__ref='704000')
        
    def get_partner_account(self,voucher):
        """
        Return the reference of the general account 
        where the partner movement of the given voucher should be booked.
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        tt = voucher.get_trade_type()
        if tt.name == 'sales':
            #~ return '4000'
            return 'customers'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'suppliers'
        
    def get_vat_account(self,tt,vc,vr):
        """
        Return the reference of the account where the VAT amount should be booked.
        `tt` is a TradeType (usually either `sales` or `purchases`)
        `vc` is a VatClass
        `vr` is a VatRegime
        
        """
        if tt.name == 'sales':
            #~ return '4000'
            return 'vat_due'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'vat_deductible'
        
        #~ return '472100'

    def get_vat_rate(self,tt,vc,vr):
        VAT_RATES = dict(
          exempt=Decimal(),
          reduced=Decimal('0.07'),
          normal=Decimal('0.20')
        )
        return VAT_RATES[vc.name]

        
        
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
        
        current_version = self.version
        
        #~ name,current_version,url = self.using().next()
        if current_version is None:
            raise Exception("Cannot migrate to version None")
        if '+' in __version__:
            raise Exception(
                "Cannot loaddata python dumps to intermediate Lino version %s" % __version__)
        if '+' in current_version:
            raise Exception(
                "Cannot loaddata python dumps to intermediate %s version %s" 
                % (self.short_name,current_version))
            #~ dblogger.info("Cannot migrate to intermediate version %", current_version)
            #~ return
            
        if globals_dict['SOURCE_VERSION'] == current_version:
            dblogger.info("Source version is %s : no migration needed", current_version)
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
                if from_version != current_version:
                    dblogger.warning("No method for migrating from version %s to %s",
                        from_version,current_version)
                break

          
    #~ def get_application_info(self):
        #~ """
        
        #~ Application developers must implement 
        #~ this in their Lino 
        #~ subclass by something like this::
        
            #~ def get_application_info(self):
                #~ from myapp import __version__, __url__
                #~ return ("MyApp",__version__,__url__)
        
        #~ This function is used by 
        #~ :meth:`using` and :meth:`site_version`.
        
        #~ """
        #~ return (self.__name__,
                #~ self.__version__,
                #~ self.__url__)
        #~ return (self.django_settings['__name__'],
                #~ self.django_settings['__version__'],
                #~ self.django_settings['__url__'])
        #~ return ("Lino App",'0.1','http://code.google.com/p/lino/')
        
        #~ raise NotImplementedError()
        
    def using(self,ui=None):
        """
        Yields a list of (name, version, url) tuples
        describing the software used on this site.
        
        The first tuple describes the application itself.
        
        This function is used by 
        :meth:`welcome_text`,
        :meth:`welcome_html`
        and
        :meth:`site_version`.
        
        """
        from lino.utils import ispure
        assert ispure(self.short_name)
        
        #~ ai = self.get_application_info()
        #~ if ai is not None:
            #~ yield ai
        if self.short_name and self.version and self.url:
            yield (self.short_name, self.version, self.url)
        
        yield ("Lino",__version__,"http://lino.saffre-rumma.net")
        
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        import jinja2
        version = getattr(jinja2,'__version__','')
        yield ("Jinja",version,"http://jinja.pocoo.org/")
        
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
        
        yield ("Silk Icons",'1.3',"http://www.famfamfam.com/lab/icons/silk/")

        if ui is not None:
            #~ version = '<script type="text/javascript">document.write(Ext.version);</script>'
            onclick = "alert('ExtJS client version is ' + Ext.version);"
            tip = "Click to see ExtJS client version"
            text = "(version)"
            #~ version = """<a href="#" onclick="%s" title="%s">%s</a>""" % (onclick,tip,text)
            version = xghtml.E.a(text,href='#',onclick=onclick,title=tip)
            yield ("ExtJS",version ,"http://www.sencha.com")
            
            if self.use_extensible:
                onclick = "alert('Extensible Calendar version is ' + Ext.ensible.version);"
                tip = "Click to see Extensible Calendar version"
                text = "(version)"
                #~ version = """<a href="#" onclick="%s" title="%s">%s</a>""" % (onclick,tip,text)
                version = xghtml.E.a(text,href='#',onclick=onclick,title=tip)
                yield ("Extensible",version ,"http://ext.ensible.com/products/calendar/")
            

    def welcome_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in self.using()]))

    def welcome_html(self,ui=None):
        """
        Text to display in the "about" dialog of a GUI application.
        """
        sep = '<br/>'
        #~ sep = ', '
        return sep.join(['<a href="%s" target="_blank">%s</a>&nbsp;%s' 
            % (u,n,v) for n,v,u in self.using(ui)])

    def site_version(self):
        """
        Used in footnote or header of certain printed documents.
        """
        name,version,url = self.using().next()
        #~ name,version,url = self.get_application_info()
        #~ if self.short_name
        #~ if self.version is None:
            #~ return self.short_name + ' (Lino %s)' % __version__
        #~ return self.short_name + ' ' + self.version
        return name + ' ' + version
        #~ return "Lino " + __version__


    #~ def watch_changes(self,model,fields=None,**options):
        #~ """
        #~ Declare a set of fields of a model to be "observed" or "watched".
        #~ Each change to an object comprising at least one watched 
        #~ will lead to an entry to the ChangesByObject table.
        
        #~ `model` may be a string `app.Model`.
        #~ It will be resolved during kernel startup.
        #~ All calls to watch_changes will be grouped by model.
        
        #~ See also :mod:`lino.utils.dblogger`.
        #~ """
        #~ self._watch_changes_requests.append((model,fields,options))
        
        
    #~ def setup_changelog(self):
    def on_site_startup(self):
        """
        This method is called during site startup
        """
        pass
        

    def get_system_note_recipients(self,ar,obj,silent):
        """
        Return or yield a list of recipients 
        (i.e. strings "Full Name <name@example.com>" )
        to be notified by email about a system note issued 
        by action request `ar` about the object instance `obj`.
        
        Default behaviour is to simply forwar it to the `obj`'s 
        :meth:`get_system_note_recipients <lino.core.model.Model.get_system_note_recipients>`,
        but here is a hook to define local exceptions to the 
        application specific default rules.
        """
        return obj.get_system_note_recipients(ar,silent)
        

    def get_todo_tables(self,ar):
        """
        Return or yield a list of tables that should be empty
        """
        for mod in self.get_installed_modules():
            meth = getattr(mod,'get_todo_tables',None)
            if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
                for i in meth(self,ar):
                    yield i

    def get_installed_apps(self):
        """
        This method is expected to return or yield the list of strings 
        to be stored into Django's :setting:`INSTALLED_APPS` setting.
        """
        if self.user_model is not None and self.remote_user_header is None:
            yield 'django.contrib.sessions' # 20121103
        #~ 'django.contrib.sites',
        #~ 'django.contrib.markup',
        yield 'lino'
        yield 'lino.modlib.about'
        #~ if self.admin_prefix:
            #~ yield 'lino.modlib.pages'
        
    #~ def get_guest_greeting(self):
        #~ return xghtml.E.p("Please log in")
        

    def build_admin_url(self,*args,**kw):
        #~ if self.admin_prefix:
            #~ return buildurl(self.admin_prefix,*args,**kw)
        #~ return buildurl(*args,**kw)
        return self.admin_prefix + buildurl(*args,**kw)
    #~ build_url = build_admin_url

    def build_media_url(self,*args,**kw):
        return buildurl('media',*args,**kw)
        
    def build_plain_url(self,*args,**kw):
        return self.plain_prefix + buildurl(*args,**kw)
        

    def get_urls(self):
        return []

    #~ def get_sidebar_html(self,request=None,node=None,**context):
        #~ pages = dd.resolve_app('pages')
        #~ return pages.get_sidebar_html(self,request=None,node=None,**context)
        
    sidebar_width = 0
    """
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.
    """