# -*- coding: UTF-8 -*-
import sys
from os.path import join

LINO_ROOT = '/var/snapshots/lino'
try:
    # make sure that there is no duplicate lino in the PYTHONPATH.
    import lino
    if not lino.__file__.startswith(LINO_ROOT):
        raise Exception("Duplicate lino module: %s is not in %s" % (lino.__file__,LINO_ROOT))
except ImportError:
    sys.path.append(LINO_ROOT)

from lino.apps.pcsw.settings import *
class Lino(Lino):
    title = u"My first Lino site"
    csv_params = dict(delimiter=',',encoding='utf-16')
    languages = ('en','fr','nl')
LINO = Lino(__file__,globals())

LINO.appy_params.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')

LOGGING = dict(filename='/var/log/lino/system.log'),level='DEBUG')
# some alternative examples:
# LOGGING = dict(filename=join(LINO.project_dir,'log','system.log'),level='DEBUG')
# LOGGING = dict(filename=None,level='DEBUG')


# MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'mysite',                  
#         'USER': 'django',                     
#         'PASSWORD': 'my cool password',               
#         'HOST': 'localhost',                  
#         'PORT': 3306,
#     }
# }

# sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite', 
        'NAME': join(LINO.project_dir,'mysite.db')
    }
}

EMAIL_HOST = "mail.example.com"
#EMAIL_PORT = ""
