# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

from django import http
from django.views.generic import View

from lino.api import dd

from lino.utils.xmlgen import html as xghtml
E = xghtml.E


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
