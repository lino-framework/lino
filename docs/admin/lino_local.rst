A `lino_local` package
======================

When hosting multiple Lino sites on a same host we suggest 
to create a directory :file:`lino_local` 
somewhere in your :doc:`Python Path </admin/pythonpath>`,
with an :file:`__init__.py` file to make it available 
as Python package,
and then create your project directories as subdirectories 
of this.

The :file:`__init__.py` of your `lino_local` package
might then have the following content (adapt to your needs, 
this is just to fire up your imagination):

.. code-block:: python

    # file /usr/local/mypy/lino_local/__init__.py
    import os, sys
    from os.path import join, split, dirname, abspath
    
    MEMORY_DB = False
    
    LOCAL_PREFIX = split(dirname(abspath(__file__)))[-1] + '.'
    # e.g. LOCAL_PREFIX will be "lino_local." 
    
    def setup(filename):
        prj = split(dirname(abspath(filename)))[-1]
        os.environ['DJANGO_SETTINGS_MODULE'] = LOCAL_PREFIX + prj + '.settings'

    def manage(filename):
        setup(filename)
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    
    class LocalLinoMixin(object):
        """
        Local settings to be mixed into Lino class definitions on this host.
        """
        
        # e.g. all Lino sites on this host are bilingual by default:
        languages = ['en','fr']
        
        # local third-party software installation paths 
        extjs_root = r's:\ext-3.3.1'
        extensible_root  = r's:\extensible-1.0.1'
        jasmine_root  = r's:\jasmine-5ca2888\lib\jasmine-core'
        bootstrap_root = r's:\bootstrap'
        beid_jslib_root  = r't:\data\luc\lino_local\dsbe\media\beid-jslib'
        
        # local Django settings
        def __init__(self,*args,**kw):
            super(LocalLinoMixin,self).__init__(*args,**kw)
            self.django_settings.update(ADMINS=[("James","james@example.com")])
            self.django_settings.update(EMAIL_HOST="mail.example.com")
            
            # 
            dbname  = join(self.project_dir,'default.db')
            if MEMORY_DB:
                dbname  = ':memory:'
            self.django_settings.update(DATABASES = {
              'default': {
                  'ENGINE': 'django.db.backends.sqlite3',
                  'NAME': dbname
              }})
            

Then in each :xfile:`settings.py` you use this as follows 
to inherit from both the application's settings (e.g. `foo.bar.settings`) 
and your `LocalLinoMixin`.

.. code-block:: python

    from foo.bar.settings import *
    from lino_local import LocalLinoMixin
    
    class Lino(LocalLinoMixin,Lino):
    
        # Lino settings for this particular site 
        languages = ['en']
        
    # Django settings for this particular site 
    DEBUG = True      


And the :xfile:`manage.py` and :xfile:`wsgi.py` of each project are the same:

.. code-block:: python

    #!/usr/bin/env python
    # file manage.py (same for each project)
    from lino_local import manage 
    manage(__file__)
      

.. code-block:: python

    # file wsgi.py (same for each project)
    from lino_local import setup ; setup(__file__)
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()      

