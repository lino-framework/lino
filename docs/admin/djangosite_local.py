# adapt to your needs, this is just to fire up your imagination

import site
import os, sys
from os.path import split, dirname, abspath, join

DEFAULT_VIRTUALENV_NAME = 'demo'
PYTHON_VERSION = (2,7)

def manage(filename,*args,**kw):
    setup_django_settings(dirname(abspath(filename)),*args,**kw)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

def setup_wsgi(globals_dict,*args,**kw):
    filename = globals_dict['__file__']
    home_dir,tail = split(dirname(abspath(filename)))
    assert tail == 'apache', "%r is not apache" % tail
    setup_django_settings(home_dir,*args,**kw)
    import django.core.handlers.wsgi
    globals_dict.update(application=django.core.handlers.wsgi.WSGIHandler())



def setup_django_settings(homedir,settings_module='settings',ve=DEFAULT_VIRTUALENV_NAME):
    site.addsitedir(homedir)
    site.addsitedir('/usr/local/pythonenv/%s/lib/python%d.%d/site-packages' % (ve,PYTHON_VERSION[0],PYTHON_VERSION[1]))
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

def setup_site(self):

    self.tinymce_base_url = None

    self.tinymce_root = '/usr/share/tinymce/www'

    self.jasmine_root  = None

    self.csv_params = dict(delimiter=',',encoding='utf-16')

    self.build_js_cache_on_startup = False

    self.django_settings.update(EMAIL_HOST='mail.example.com')
    self.django_settings.update(ALLOWED_HOSTS=['.example.com'])
    self.django_settings.update(EMAIL_SUBJECT_PREFIX='['+self.project_name+'] ')
    self.django_settings.update(SERVER_EMAIL='noreply@example.com')
    self.django_settings.update(DEFAULT_FROM_EMAIL='noreply@example.com')
    self.django_settings.update(ADMINS=[["John Doe", "john@example.com"]])
    self.django_settings.update(DEBUG=False)
    self.django_settings.update(SECRET_KEY='?~hdakl123ASD%#¤/&¤')

    self.site_config_defaults = dict(default_build_method='appypdf')

    self.appy_params.update(ooPort=8100)
    #        pythonWithUnoPath='/etc/openoffice.org3/program/python')

