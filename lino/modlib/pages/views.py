# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

import os
import cgi

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
#~ from django.utils import simplejson as json
import json
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils.encoding import force_unicode

from lino import dd, rt
#~ from lino.core.signals import pre_ui_delete

from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.utils.jsgen import py2js
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import isiterable
from lino.utils import dblogger
from lino.core import auth

from lino.core import actions
from lino.core import dbtables
#~ from lino.core import changes
from lino.core.dbutils import navinfo

from lino.ui.views import requested_actor, action_request
from lino.ui.views import json_response, json_response_kw

#~ from lino.ui import requests as ext_requests
from lino.core import constants as ext_requests
from lino.ui import elems as ext_elems

from django import http
from django.views.generic import View

from lino import dd, rt
pages = dd.resolve_app('pages')


class PagesIndex(View):

    def get(self, request, ref='index'):
        if not ref:
            ref = 'index'

        #~ print 20121220, ref
        obj = pages.lookup(ref, None)
        if obj is None:
            raise http.Http404("Unknown page %r" % ref)
        html = pages.render_node(request, obj)
        return http.HttpResponse(html)
