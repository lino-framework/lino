# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

#~ from django.db import models
#~ from django.http import HttpResponse, Http404
#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
#~ from django.utils import simplejson as json
#~ from django.conf import settings


_handle_attr_name = '_lino_ui_handle'


CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"


URL_PARAM_PROJECT = 'prj'
URL_PARAM_TEAM_VIEW = 'tv'
URL_PARAM_END_DATE = 'ed'
URL_PARAM_START_DATE = 'sd'

URL_PARAM_PARAM_VALUES = 'pv'
URL_PARAM_FIELD_VALUES = 'fv'

URL_PARAM_ACTION_NAME = 'an'

URL_PARAM_FORMAT = 'fmt'
URL_PARAM_REQUESTING_PANEL = 'rp'

URL_PARAM_MASTER_TYPE = 'mt'
"""
The pk of the ContentType of the master model.
"""

URL_PARAM_MASTER_PK = 'mk'
"""
The pk of the master instance.
"""

URL_PARAM_USER_LANGUAGE = 'ul'
"""
override user language
"""


#~ URL_PARAM_EUSER = 'euser'
#~ URL_PARAM_EUSER = 'su'

URL_PARAM_SUBST_USER = 'su'
"""
substitute user
"""

URL_PARAM_KNOWN_VALUES = 'kv'
"""
known values
"""

URL_PARAM_ACTION_STEP = "as"

# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_GRIDFILTER = 'filter'
URL_PARAM_FILTER = 'query'
URL_PARAM_TAB = 'tab'
#~ URL_PARAM_EXPAND = 'expand'
#~ """
#~ A string entered in the quick search field or in the text field of a combobox.
#~ """

URL_PARAM_SORT = 'sort'
URL_PARAM_SORTDIR = 'dir'
URL_PARAM_START = 'start'
URL_PARAM_LIMIT = 'limit'
URL_PARAM_WIDTHS = 'cw'
URL_PARAM_HIDDENS = 'ch'
URL_PARAM_COLUMNS = 'ci'
URL_PARAM_SHOW_PARAMS_PANEL = 'sp'
#~ TEST = 'name'

URL_PARAM_SELECTED = 'sr'

URL_PARAMS = [
    'URL_PARAM_ACTION_NAME',
    'URL_PARAM_FORMAT',
    'URL_PARAM_MASTER_TYPE',
    'URL_PARAM_MASTER_PK',
    'URL_PARAM_GRIDFILTER',
    'URL_PARAM_FILTER',
    'URL_PARAM_SORT',
    'URL_PARAM_SORTDIR',
    'URL_PARAM_START',
    'URL_PARAM_LIMIT',
    'URL_PARAM_TAB',
    'URL_PARAM_REQUESTING_PANEL',
    'URL_PARAM_SHOW_PARAMS_PANEL',
    'URL_PARAM_SUBST_USER',
    'URL_PARAM_USER_LANGUAGE',
    'URL_PARAM_ACTION_STEP',
    'URL_PARAM_SELECTED',
    #~ 'TEST',
]

#~ URL_PARAM_CHOICES_PK = "ck"

#~ FMT_RUN = 'act'
#~ FMT_JSON = 'json'

#~ User = reports.resolve_model('users.User')
#~ from lino.modlib.users.models import User

URL_FORMAT_JSON = 'json'
URL_FORMAT_PDF = 'pdf'
URL_FORMAT_ODT = 'odt'
URL_FORMAT_PRINTER = 'printer'
URL_FORMAT_HTML = 'html'


def dict2kw(d):
    newd = {}
    for k, v in d.items():
        newd[str(k)] = v
    return newd


def authenticated_user(user):
    #~ if user.is_anonymous():
        #~ return None
    return user


def parse_boolean(v):
    if v in ('true', 'on', True):
        return True
    if v in ('false', 'off', False):
        return False
    #~ raise Exception("Invalid boolean value %r for field %s" % (v,self.name))
    raise Exception("Invalid boolean value %r" % v)
