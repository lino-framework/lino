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

from __future__ import unicode_literals

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

from .utils import AttrDict

execfile(os.path.join(os.path.dirname(__file__),'version.py'))

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
__url__ = "http://www.lino-framework.org"


__copyright__ = """\
Copyright (c) 2002-2013 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

NOT_FOUND_MSG = '(not installed)'


class Site(object):
    """
    Base class for the Site instance to be stored in :setting:`SITE`.
    
    This simple trick brings inheritance to the settings and 
    lets us define methods and override them in local `settings.py` 
    files.
    
    This class is first defined in :mod:`django_site`, 
    subclassed by :mod:`lino`, 
    then usually subclassed by the application developer
    (e.g. :mod:`lino.projects.cosi.Lino`),
    then imported into your local :xfile:`settings.py`,
    where you may subclass it another time before 
    finally instantiating it, and assigning it to 
    the :setting:`SITE` variable.
    
    Instiatiation is always the same line of code::
    
      SITE = Site(__file__,globals())
      
    With the parameters `__file__` and `globals()` you give Lino 
    information about your local settings (where they are in the file 
    system), and the possibility to modify your Django settings.
    
    During instantiation the `Site` will modify the following Django settings 
    (which means that if you want to modify one of these, 
    do it *after* instantiating your :setting:`SITE`):
    
      :setting:`ROOT_URLCONF`
      :setting:`SERIALIZATION_MODULES`
      :setting:`MEDIA_ROOT` 
      :setting:`TEMPLATE_DIRS`
      :setting:`FIXTURE_DIRS` 
      :setting:`LOGGING_CONFIG`
      :setting:`LOGGING`
      :setting:`MIDDLEWARE_CLASSES`
      :setting:`TEMPLATE_LOADERS`
      ...
    
    """
    
    make_missing_dirs = True
    """
    Set this to False if you don't want Lino to automatically 
    create missing dirs when needed 
    (but to raise an exception in these cases, asking you to create it yourself)
    """
    
    help_url = "http://code.google.com/p/lino"
    #~ site_url = 
    #~ index_html = "This is the main page."
    #~ title = None
    title = "Unnamed Django site"
    #~ domain = "www.example.com"
    
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
    
    description = """
    yet another <a href="%s">Django-Sites</a> application.""" % __url__
    """
    A short single-sentence description.
    It should start with a lowercase letter because the beginning 
    of the sentence will be generated from other class attributes 
    like :attr:`short_name` and :attr:`version`.
    """
    
    is_local_project_dir = False
    """
    This is automatically set when a :class:`Lino` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """
    
    
    migration_module = None
    """
    If you maintain a data migration module for your application, 
    specify its name here.
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
    
    site_config = None
    """
    ui.Lino overrides this to hold a SiteConfig instance.
    """
    
    modules = AttrDict()
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
    
    startup_time = None
    """
    Don't modify this. 
    It contains the time when this this Lino has been instantiated,
    iaw the startup time of this Django process.
    """
    
    
    def __init__(self,project_file,django_settings):
        if django_settings.has_key('LINO'):
            raise Exception("Oops: rename settings.LINO to settings.SITE")
        if django_settings.has_key('Lino'):
            raise Exception("Oops: rename settings.Lino to settings.Site")
            
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        
        #~ self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        #~ self._starting_up = False
        self._startup_done = False
        #~ self._response = None
        self.django_settings = django_settings
        
        django_settings.update(SERIALIZATION_MODULES = {
            "py" : "lino.utils.dumpy",
        })
        
        self.startup_time = datetime.datetime.now()
        
        django_settings.update(DATABASES= {
              'default': {
                  'ENGINE': 'django.db.backends.sqlite3',
                  'NAME': join(self.project_dir,'default.db')
              }
            })
            
        
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
          
       

    #~ def add_dummy_message(self,s):
        #~ self.dummy_messages.add(s)

    #~ def get_app_source_file(self):
        #~ "Override this in each application"
        #~ return __file__
        
    #~ def analyze_models(self):
        #~ from lino.core.kernel import analyze_models
        #~ analyze_models()
        
    def startup(self,**options):
        """
        Start the Lino instance (the object stored as :setting:`LINO` in 
        your :xfile:`settings.py`).
        This is called exactly once from :mod:`lino.models` 
        when Django has has populated it's model cache.
        
        This code can run several times at once when running e.g. under mod_wsgi: 
        another thread has started and not yet finished `startup()`.
        
        """
        if self._startup_done:
            #~ # logger.info("Lino startup already done")
            return
            
        self._startup_done = True
        
        self.do_site_startup()
        
    def do_site_startup(self):
        """
        This method is called during site startup
        """
        pass
        
    def is_installed_model_spec(self,model_spec):
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

        
    
    def makedirs_if_missing(self,dirname):
        """
        Make missing directories if they don't exist 
        and if :attr:`make_missing_dirs` is `True`.
        """
        #~ if not os.path.exists(dirname):
            #~ os.makedirs(dirname)
        if not os.path.isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" % dirname)
        
    
        
        
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


    #~ def get_installed_modules(self):
        #~ from django.conf import settings
        #~ from django.utils.importlib import import_module
        #~ from django.utils.module_loading import module_has_submodule
        #~ for app_name in settings.INSTALLED_APPS:
            #~ app_module = import_module(app_name)
            #~ if module_has_submodule(app_module, 'models'):
                #~ yield import_module('.models', app_module)
        
    def on_each_app(self,methname,*args):
        """
        Call the named method on each module in :setting:`INSTALLED_APPS`
        that defines it.
        """
        from lino.utils import dblogger
        #~ for mod in self.get_installed_modules():
        from django.db.models import loading
        for mod in loading.get_apps():
            meth = getattr(mod,methname,None)
            if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
                meth(self,*args)

    def demo_date(self,days=0,**offset):
        """
        Used e.g. in python fixtures.
        """
        if days:
            offset.update(days=days)
        #~ J = datetime.date(2011,12,16)
        if offset:
            return self.startup_time.date() + datetime.timedelta(**offset)
        return self.startup_time.date()
        
        
    def install_migrations(self,*args):
        """
        See :func:`lino.utils.dumpy.install_migrations`.
        """
        from lino.utils.dumpy import install_migrations
        install_migrations(self,*args)
          
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
        
        if self.short_name and self.version and self.url:
            yield (self.short_name, self.version, self.url)
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python",version,"http://www.python.org/")
        
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        yield ("DjangoSite",__version__,"http://www.lino-framework.org")
        

    def welcome_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in self.using()]))

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


            