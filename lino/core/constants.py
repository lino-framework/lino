# Copyright 2009-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines explicit code names for URL parameters

"""
# import six
# str = six.text_type
from builtins import str

_handle_attr_name = '_lino_ui_handle'


CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"


URL_PARAM_PROJECT = 'prj'
URL_PARAM_TEAM_VIEW = 'tv'
URL_PARAM_END_DATE = 'ed'
URL_PARAM_START_DATE = 'sd'

URL_PARAM_PARAM_VALUES = 'pv'
"""Array of values of table parameters."""

URL_PARAM_FIELD_VALUES = 'fv'
"""Array of values of action parameters."""

URL_PARAM_ACTION_NAME = 'an'

URL_PARAM_FORMAT = 'fmt'
URL_PARAM_REQUESTING_PANEL = 'rp'

URL_PARAM_MASTER_TYPE = 'mt'
"""The content type of the master instance.

"""

URL_PARAM_MASTER_PK = 'mk'
"""The primary key of the master instance.
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

URL_PARAM_LINO_VERSION = "lv"
"""Version number of linoweb.js for version clash checking"""

URL_PARAM_DEVICE_TYPE = 'dt'
"""
Connected device type (used by Openui5)
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
"""The number of the active tab panel.
"""

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
    'URL_PARAM_LINO_VERSION',
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


#~ DEFAULT_GC_NAME = 'std'
DEFAULT_GC_NAME = 0


ICON_NAMES = """
arrow_join arrow_up arrow_down delete add book_link eye basket
emoticon_smile pencil cross money
application_form application_view_list application_view_detail
disk hourglass date_add email_add email_go script script_add bell calendar
printer lightning printer_delete arrow_divide
page_white_acrobat page_excel
html vcard vcard_add wrench transmit
accept database_gear
cancel flag_green date_next
""".split()
"""
A list of all names allowed as
:attr:`lino.core.actions.Action.icon_name`.
"""

# pdf --> page_white_acrobat
# csv -> page_excel


def dict2kw(d):
    newd = {}
    for k, v in list(d.items()):
        newd[str(k)] = v
    return newd


def parse_boolean(v):
    if v in ('true', 'on', True):
        return True
    if v in ('false', 'off', False):
        return False
    raise Exception("Invalid boolean value %r" % v)
