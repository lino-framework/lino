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
from lino.utils import AttrDict


#~ from lino import Lino
import lino 

class Lino(lino.Lino):
    """
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
    in :func:`lino.core.kernel.startup_site`: 
    if becomes `False` if
    either :func:`lino.core.modeltools.is_devserver` returns True
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
    Leave this unchanged as long as :dmodules
    oc:`/ticket/70` is not solved.
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
    these files yourself.
    Set this to `None`, set :attr:`extjs_root` 
    (or a symbolic link "extjs" in your :xfile:`media` directory)
    to point to the local directory  where ExtJS 3.3.1 is installed).
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
    
    
    # for internal use:
    
    #~ _extjs_ui = None
    #~ _groph_ui = None
    
    _site_config = None
    
    
    
    def __init__(self,project_file,django_settings):
        lino.Lino.__init__(self,project_file,django_settings)
        
        installed_apps = tuple(self.get_installed_apps()) + ('lino',)
        django_settings.update(INSTALLED_APPS=installed_apps)
        
        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = not modname in installed_apps
        #~ print "20130117 (not %r in %r) --> %s" % (modname , installed_apps,self.is_local_project_dir)
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
        
        
      
        if self.webdav_url is None:
            self.webdav_url = '/media/webdav/'
        if self.webdav_root is None:
            self.webdav_root = join(abspath(self.project_dir),'media','webdav')
            
        django_settings.update(MEDIA_ROOT = join(self.project_dir,'media'))
        
        django_settings.update(
            ROOT_URLCONF = 'lino.ui.urls'
          
        )
        django_settings.update(
            MIDDLEWARE_CLASSES=tuple(self.get_middleware_classes()))
                
        django_settings.update(
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
            #~ django_settings.update(TEMPLATE_LOADERS = tuple(tl))
                
                
        tcp = []
        if self.user_model == 'auth.User':
            django_settings.update(LOGIN_URL = '/accounts/login/')
            django_settings.update(LOGIN_REDIRECT_URL = "/")
            tcp += [ 'django.contrib.auth.context_processors.auth' ]
            
        tcp += [
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
            #    'django.core.context_processors.request',
                #~ 'django.contrib.messages.context_processors.messages',
        ]
        django_settings.update(TEMPLATE_CONTEXT_PROCESSORS = tuple(tcp))

    def on_site_startup(self):
        super(Lino,self).on_site_startup()
        from .ui import ExtUI
        self.ui = ExtUI()
        
    #~ @property
    #~ def ui(self):
        #~ if self._extjs_ui is None:
            #~ from .ui import ExtUI
            #~ self._extjs_ui = ExtUI()
        #~ return self._extjs_ui
    #~ ui = property(get_ui)

    #~ def get_groph_ui(self):
        #~ if self._groph_ui is None:
            #~ self.startup()
            #~ from lino.ui.groph.groph_ui import UI
            #~ self._groph_ui = UI()
        #~ return self._groph_ui
    #~ groph_ui = property(get_groph_ui)

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
    
    def site_header(self):
        """
        Used e.g. in footnote or header of certain printed documents.
        """
        if self.is_installed('contacts'):
            if self.site_config.site_company:
                return self.site_config.site_company.address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return s

    def setup_main_menu(self):
        """
        To be implemented by applications.
        """
        pass

        
    #~ def get_site_config(self):
      
    @property
    def site_config(self):
        """
        Returns the one and only :class:`lino.models.SiteConfig` instance.
        
        If no instance exists (which happens in a virgin database),
        we create it and set some default values from 
        :attr:`site_config_defaults`.
        
        We cannot save here because it's possible that the database 
        doesn't yet exist.
        """
        if self._site_config is None:
            #~ print '20120801 create _site_config'
            from .models import SiteConfig
            from django.db.utils import DatabaseError
            try:
                self._site_config = SiteConfig.objects.get(pk=1)
            except (SiteConfig.DoesNotExist,DatabaseError):
            #~ except Exception,e:
                kw = dict(pk=1)
                #~ kw.update(settings.LINO.site_config_defaults)
                kw.update(self.site_config_defaults)
                #~ logger.debug("Creating SiteConfig record (%s)",e)
                self._site_config = SiteConfig(**kw)
            
                # 20120725 
                # polls_tutorial menu selection `Config --> Site Parameters` 
                # said "SiteConfig 1 does not exist"
                # cannot save the instance here because the db table possibly doesn't yet exit.
                #~ self._site_config.save()
        return self._site_config
    #~ site_config = property(get_site_config)
    
    def unused_update_site_config(self,**kw):
        """
        Update and save the one and only :class:`lino.models.SiteConfig` instance.
        """
        #~ print '20120801 update_site_config', kw
        sc = self.site_config
        for k,v in kw.items():
            setattr(sc,k,v)
        #~ sc.full_clean() # caused problems like ValidationError: {'sector': [u'Modell Sektor mit dem Prim\xe4rschl\xfcssel 45 ist nicht vorhanden.'], ...}        
        
        
        #~ sc.save()
        #~ self.on_site_config_saved(sc)
    
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
        #~ if self.admin_prefix:
            #~ return buildurl(self.admin_prefix,*args,**kw)
        #~ return buildurl(*args,**kw)
        return self.admin_prefix + buildurl(*args,**kw)
    #~ build_url = build_admin_url

    def build_media_url(self,*args,**kw):
        return buildurl('media',*args,**kw)
        
    def build_plain_url(self,*args,**kw):
        return self.plain_prefix + buildurl(*args,**kw)
        
    def build_extjs_url(self,url):
        if self.extjs_base_url:
            return self.extjs_base_url + url
        return self.build_media_url('extjs',url)
        

    def unused_get_urls(self):
        return []

    #~ def get_sidebar_html(self,request=None,node=None,**context):
        #~ pages = dd.resolve_app('pages')
        #~ return pages.get_sidebar_html(self,request=None,node=None,**context)
        
    sidebar_width = 0
    """
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.
    """
    
    
