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

from os.path import join, abspath, dirname, normpath, isdir
from decimal import Decimal

from urllib import urlencode

def buildurl(*args,**kw):
    url = '/' + ("/".join(args))
    if len(kw):
        url += "?" + urlencode(kw)
    return url


from lino.utils.xmlgen import html as xghtml
from lino.utils import AttrDict


import lino

class Site(lino.Site):
    """
    """
    
    partners_app_label = 'contacts'
    """
    Temporary setting, see :doc:`/tickets/72`
    """
    
    # three constants used by lino.modlib.workflows:
    max_state_value_length = 20 
    max_action_name_length = 50
    max_actor_name_length = 100
    
    #~ def add_config_value(self,name,default,help_text):
        #~ if not hasattr(self,name):
            #~ setattr(self,name,default)
    
    #~ add_config_value('allow_duplicate_cities',False)
    
    allow_duplicate_cities = False
    """
    In a default configuration (when :attr:`allow_duplicate_cities` is False), 
    Lino declares a UNIQUE clause 
    for :class:`Cities <lino.modlib.countries.models.Cities>` 
    to make sure that your database never contains duplicate cities.
    This behaviour mighr disturb e.g. when importing legacy data that 
    did not have this restriction.
    Set it to True to remove the UNIQUE clause.
    
    Changing this setting might affect your database structure 
    and thus require a :doc:`/topics/datamig`
    if your application uses :mod:`lino.modlib.countries`.
    
    """
    
    
    uid = 'myuid'
    """
    A universal identifier for this Site. 
    This is needed when synchronizing with CalDAV server.  
    Locally created calendar components in remote calendars 
    will get a UID based on this parameter,
    using ``"%s@%s" (self.pk,settings.SITE.ui)``.
    
    The default value is ``'myuid'``, and
    you should certainly override this 
    on a production server that uses remote calendars.
    """
    
    #~ person_model = None
    #~ person_model = "contacts.Person"
    #~ """
    #~ If your application uses :model:`lino.modlib.contacts`,
    #~ set this to a string "applabel.Modelname" which identifies 
    #~ your Person model (which should inherit from
    #~ :class:`lino.modlib.contacts.models.Person`).
    #~ """
    
    #~ company_model = None
    #~ company_model = "contacts.Company"
    #~ """
    #~ If your application uses :model:`lino.modlib.contacts`,
    #~ set this to a string "applabel.Modelname" which identifies 
    #~ your Company model (which should inherit from
    #~ :class:`lino.modlib.contacts.models.Company`).
    #~ """
    
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
    
    
    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy database.    
    """
    
    propvalue_max_length = 200
    """
    Used by :mod:`lino.modlib.properties`.
    """
    
    
    
    never_build_site_cache = False
    """
    Set this to `True` if you want that Lino 
    never (re)builds the site cache (even when asked). 
    This can be useful on a development server when you are debugging 
    directly on the generated :xfile:`lino*.js`.
    Or for certain unit test cases.
    """
    
    show_internal_field_names = False
    """
    Whether the internal field names should be visible.
    Default is `False`.
    ExtUI implements this by prepending them to the tooltip,
    which means that :attr:`use_quicktips` must also be `True`.
    """
    
    build_js_cache_on_startup = None
    """
    Whether the Javascript cache files should be built on startup 
    for all user profiles and languages.
    
    On a production server this should be `True` for best performance,
    but while developing, it may be easier to set it to `False`, which means 
    that each file is built upon need (when a first request comes in).
    
    The default value `None` means that Lino decides automatically 
    during startup:
    it becomes `False` if
    either :func:`lino.core.dbutils.is_devserver` returns True
    or setting:`DEBUG` is set.
    """
    
    #~ replace_django_templates = True
    #~ """
    #~ Whether to replace Djano's template engine by Jinja.
    #~ """
    
    use_experimental_features = False
    """
    Whether to include "experimental" features.
    """
    
    site_config_defaults = {}
    """
    Default values to be used when creating the 
    :class:`lino.models.SiteConfig` instance.
    
    Usage example::
    
      site_config_defaults = dict(default_build_method='appypdf')
      
    """
    
    
    use_spinner = False # doesn't work. leave this to False
    
    #~ django_admin_prefix = '/django' 
    django_admin_prefix = None
    """
    The prefix to use for Django admin URLs.
    Leave this unchanged as long as :doc:`/ticket/70` is not solved.
    """
    
    plain_prefix = '/plain' 
    """
    The prefix to use for the "plain html" URLs.
    """
    
    #~ admin_url = 'admin/'
    #~ admin_prefix = '/admin'
    #~ admin_url = '' # 
    admin_prefix = '' 
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
    
    use_extjs = True
    
    time_format_extjs = 'H:i'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
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
    
    #~ default_number_format_extjs = '0,000.00/i'
    default_number_format_extjs = '0,00/i'
    
    uppercase_last_name = False
    """
    Whether last name of persons should be printed with uppercase letters.
    See :mod:`lino.test_apps.human`
    """
    
    extjs_root = None
    """
    Path to the ExtJS root directory. 
    Only used when :attr:`extjs_base_url` is None,
    and when the `media` directory has no symbolic link named `extjs` 
    pointing to the ExtJS root directory.
    """
    
    extjs_base_url = "http://extjs-public.googlecode.com/svn/tags/extjs-3.3.1/release/"
    """
    The URL from where to include the ExtJS library files.
    
    The default value points to the 
    `extjs-public <http://code.google.com/p/extjs-public/>`_
    repository and thus requires the clients to have an internet 
    connection.
    This relieves newcomers from the burden of having to 
    specify a download location in their :xfile:`settings.py`.
    
    On a production site you'll probably want to download and serve 
    these files yourself by setting this to `None` and 
    setting :attr:`extjs_root` 
    (or a symbolic link "extjs" in your :xfile:`media` directory)
    to point to the local directory  where ExtJS 3.3.1 is installed).
    
    The same rules apply to the attributes
    :attr:`extensible_base_url <lino.ui.Site.extensible_base_url>`, 
    :attr:`bootstrap_base_url <lino.ui.Site.bootstrap_base_url>` and
    :attr:`tinymce_base_url <lino.ui.Site.tinymce_base_url>`.
    """
    
    extensible_base_url = "http://ext.ensible.com/deploy/1.0.2/"
    "Similar to :attr:`extjs_base_url` but pointing to ext.ensible.com."
    
    bootstrap_base_url = "http://twitter.github.com/bootstrap/assets/"
    "Similar to :attr:`extjs_base_url` but pointing to twitter.github.com."
    
    tinymce_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"
    "Similar to :attr:`extjs_base_url` but pointing to http://www.tinymce.com."
    
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
    The UserProfile to be assigned to anonymous user.
    
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
    
    use_davlink = False
    """
    Set this to `False` if you don't need WebDAV-enabled links.
    """
    
    max_auto_events = 36
    """
    Maximum number of automatic events to be generated 
    by :class:`lino.modlib.cal.models.EventOwner`.
    """
    
    #~ mergeable_models = []
    #~ """
    #~ A list of models that should have a "Merge" action
    #~ (see :mod:`lino.mixins.mergeable`).
    #~ """
    
    override_modlib_models = []
    """
    A list of names of modlib models which are being 
    redefined by this application.
    
    The following modlib models currently support this:
    - :class:`contacts.Person <lino.modlib.contacts.models.Person>`
    - :class:`contacts.Company <lino.modlib.contacts.models.Company>`
    
    Usage: in your application's `settings.py`, specify::
    
      class Site(Site):
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
    
    sidebar_width = 0
    """
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.
    """
    
    
    # for internal use:
    
    #~ _extjs_ui = None
    #~ _groph_ui = None
    
    _site_config = None
    
    def init_nolocal(self,*args):
        super(Site,self).init_nolocal(*args)
    
        installed_apps = tuple(self.get_installed_apps()) + ('lino','djangosite')
        self.update_settings(INSTALLED_APPS=installed_apps)
        
        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = not modname in installed_apps
            
        """
        If your project_dir contains no :xfile:`models.py`, 
        but *does* contain a `fixtures` subdir, 
        then Lino automatically adds this as "local fixtures directory" 
        to Django's `FIXTURE_DIRS`.
        """
        if self.is_local_project_dir:
            pth = join(self.project_dir,'fixtures')
            if isdir(pth):
                self.update_settings(FIXTURE_DIRS = [pth])
                
        if self.webdav_url is None:
            self.webdav_url = '/media/webdav/'
        if self.webdav_root is None:
            self.webdav_root = join(abspath(self.project_dir),'media','webdav')
            
        self.update_settings(MEDIA_ROOT = join(self.project_dir,'media'))
        
        self.update_settings(
            ROOT_URLCONF = 'lino.ui.urls'
          
        )
        self.update_settings(
            MIDDLEWARE_CLASSES=tuple(self.get_middleware_classes()))
                
        self.update_settings(
            TEMPLATE_LOADERS=tuple([
                'lino.core.web.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                #~ 'django.template.loaders.eggs.Loader',
                ]))
           
        #~ else:
            #~ tl = [
                #~ 'django.template.loaders.filesystem.Loader',
                #~ 'django.template.loaders.app_directories.Loader',
                #     'django.template.loaders.eggs.load_template_source',
            #~ ]
            #~ self.update_settings(TEMPLATE_LOADERS = tuple(tl))
                
                
        tcp = []
        if self.user_model == 'auth.User':
            self.update_settings(LOGIN_URL = '/accounts/login/')
            self.update_settings(LOGIN_REDIRECT_URL = "/")
            tcp += [ 'django.contrib.auth.context_processors.auth' ]
            
        tcp += [
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
            #    'django.core.context_processors.request',
                #~ 'django.contrib.messages.context_processors.messages',
        ]
        self.update_settings(TEMPLATE_CONTEXT_PROCESSORS = tuple(tcp))
       
    def do_site_startup(self):
        super(Site,self).do_site_startup()
        #~ raise Exception("20130302")
        #~ try:
        if True:
            from .ui import ExtUI
            self.ui = ExtUI()
        #~ except Exception as e:
            #~ import traceback
            #~ traceback.print_exc(e)
            #~ sys.exit(-10)
        #~ raise Exception("20130302")
        

    def is_abstract_model(self,name):
        """
        Return True if the named model ("myapp.MyModel") is declared in 
        :attr:`override_modlib_models`.
        """
        return name in self.override_modlib_models
        
    def is_imported_partner(self,obj):
        """
        Return whether the specified
        :class:`Partner <lino.modlib.contacts.models.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
                  
        
    def site_header(self):
        """
        Used in footnote or header of certain printed documents.
        
        The convention is to call it as follows from an appy.pod template
        (use the `html` function, not `xhtml`)
        ::
        
          do text
          from html(settings.SITE.site_header())
          
        Note that this is expected to return a unicode string possibly 
        containing valid HTML (not XHTML) tags for formatting. 
        
        
        """
        if self.is_installed('contacts'):
            if self.site_config.site_company:
                return self.site_config.site_company.address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return ''
        

    def setup_main_menu(self):
        """
        To be implemented by applications.
        """
        pass

        
      
    @property
    def site_config(self):
        """
        Returns the one and only :class:`lino.models.SiteConfig` instance.
        
        If no instance exists (which happens in a virgin database),
        we create it using default values from :attr:`site_config_defaults`.
        
        This property may not be used as long as there is no database 
        connected (or not initialized).
        
        """
        if self._site_config is None:
            #~ raise Exception(20130301)
            #~ print '20120801 create _site_config'
            from lino.core.dbutils import resolve_model
            #~ from lino.utils import dblogger as logger
            SiteConfig = resolve_model('ui.SiteConfig')
            #~ from .models import SiteConfig
            #~ from django.db.utils import DatabaseError
            try:
                self._site_config = SiteConfig.objects.get(pk=1)
                #~ logger.info("20130301 Loaded SiteConfig record (%s)",self._site_config)
            #~ except (SiteConfig.DoesNotExist,DatabaseError):
            except SiteConfig.DoesNotExist:
            #~ except Exception,e:
                kw = dict(pk=1)
                #~ kw.update(settings.SITE.site_config_defaults)
                kw.update(self.site_config_defaults)
                self._site_config = SiteConfig(**kw)
                #~ logger.info("20130301 Created SiteConfig record (%s)",self._site_config)
                # 20120725 
                # polls_tutorial menu selection `Config --> Site Parameters` 
                # said "SiteConfig 1 does not exist"
                # cannot save the instance here because the db table possibly doesn't yet exit.
                #~ self._site_config.save()
        return self._site_config
    #~ site_config = property(get_site_config)
    
    def clear_site_config(self):
        """
        Clear the cached SiteConfig instance. 
        
        This is needed e.g. when the test runner has created the test database.
        """
        self._site_config = None
    
    def on_site_config_saved(self,sc):
        """
        Used internally. Called by SiteConfig.save() to update the cached instance.
        """
        self._site_config = sc
        #~ print '20120801 site_config saved', sc.propgroup_softskills
        
    def is_imported_partner(self,obj):
        """
        Return whether the specified
        :class:`Partner <lino.modlib.contacts.models.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
        
        
    def get_quicklinks(self,ar):
        from lino.core import menus
        m = menus.Toolbar(ar.get_user().profile,'quicklinks')
        self.setup_quicklinks(ar,m)
        return m
        
    def get_site_menu(self,ui,profile):
        """
        Return this site's main menu for the given UserProfile. 
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
        #~ main.add_url_button(url,label=_("Home"))
        #~ url = "javascript:Lino.close_all_windows()"
        #~ main.add_url_button(url,label=_("Home"))
        return main
        
    def setup_quicklinks(self,ar,m):
        """
        Override this 
        in application-specific (or even local) :xfile:`settings.py` files 
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.projects.pcsw.settings.Site.setup_quicklinks`.
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


    def get_middleware_classes(self):
        """
        Yields the strings to be stored in 
        the :setting:`MIDDLEWARE_CLASSES` setting.
        
        In case you don't want to use this method
        for defining :setting:`MIDDLEWARE_CLASSES`, 
        you can simply set :setting:`MIDDLEWARE_CLASSES`
        in your :xfile:`settings.py` 
        after the :class:`lino.Site` has been initialized.
        
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
    #~ `user_model` is not None, but no `remote_user_header` in your settings.SITE.""")
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
        
    
    def get_main_html(self,request):
        """
        Return a chunk of html to be displayed in the main area of the admin index.
        This is being called only if :meth:`get_main_action` returns `None`.
        The default implementation returns the message 
        "You are now in the admin section..."
        """
        from lino.core import web
        return web.render_from_request(request,'admin_main.html')


    def get_installed_apps(self):
        """
        This method is expected to return or yield the list of strings 
        to be stored into Django's :setting:`INSTALLED_APPS` setting.
        """
        yield 'lino.ui'
        if self.user_model is not None and self.remote_user_header is None:
            yield 'django.contrib.sessions' # 20121103
        if self.django_admin_prefix:
            yield 'django.contrib.admin'
        #~ 'django.contrib.markup',
        #~ yield 'django_extensions'
        yield 'lino.modlib.about'
        #~ if self.admin_prefix:
            #~ yield 'lino.modlib.pages'
        
    #~ def get_guest_greeting(self):
        #~ return xghtml.E.p("Please log in")
        

    def build_admin_url(self,*args,**kw):
        return self.admin_prefix + buildurl(*args,**kw)

    def build_media_url(self,*args,**kw):
        return buildurl('media',*args,**kw)
        
    def build_plain_url(self,*args,**kw):
        return self.plain_prefix + buildurl(*args,**kw)
        
    def build_extjs_url(self,url):
        if self.extjs_base_url:
            return self.extjs_base_url + url
        return self.build_media_url('extjs',url)
        
    def build_extensible_url(self,url):
        if self.extensible_base_url:
            return self.extensible_base_url + url
        return self.build_media_url('extensible',url)
        
    def build_bootstrap_url(self,url):
        if self.bootstrap_base_url:
            return self.bootstrap_base_url + url
        return self.build_media_url('bootstrap',url)
        
    def build_tinymce_url(self,url):
        if self.tinymce_base_url:
            return self.tinymce_base_url + url
        return self.build_media_url('tinymce',url)
        
    
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
        

    def using(self,ui=None):
        for u in super(Site,self).using(ui): yield u
            
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
            yield ("Silk Icons",'1.3',"http://www.famfamfam.com/lab/icons/silk/")

            
          

    def welcome_html(self,ui=None):
        """
        Text to display in the "about" dialog of a GUI application.
        """
        sep = '<br/>'
        #~ sep = ', '
        return sep.join(['<a href="%s" target="_blank">%s</a>&nbsp;%s' 
            % (u,n,v) for n,v,u in self.using(ui)])

