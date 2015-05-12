# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from lino.core import constants as ext_requests
from lino.core.renderer import HtmlRenderer
from lino.core.renderer import add_user_language


class Renderer(HtmlRenderer):

    """A  HTML render that uses Bootstrap3.

    """

    # is_interactive = True

    def instance_handler(self, ar, obj, **kw):
        a = obj.get_detail_action(ar)
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar, obj, None):
                add_user_language(kw, ar)
                return self.get_detail_url(obj, **kw)

    #~ def href_to(self,ar,obj,text=None):
        #~ h = self.instance_handler(ar,obj)
        #~ if h is None:
            #~ return cgi.escape(force_unicode(obj))
        #~ return self.href(url,text or cgi.escape(force_unicode(obj)))

    def pk2url(self, ar, pk, **kw):
        if pk is not None:
            return self.plugin.build_plain_url(
                ar.actor.model._meta.app_label,
                ar.actor.model.__name__,
                str(pk), **kw)

    def get_detail_url(self, obj, *args, **kw):
        return self.plugin.build_plain_url(
            obj._meta.app_label,
            obj.__class__.__name__,
            str(obj.pk), *args, **kw)

    def get_home_url(self, *args, **kw):
        return self.plugin.build_plain_url(*args, **kw)

    def get_request_url(self, ar, *args, **kw):
        if ar.actor.__name__ == "Main":
            return self.plugin.build_plain_url(*args, **kw)

        st = ar.get_status()
        kw.update(st['base_params'])
        add_user_language(kw, ar)
        if ar.offset is not None:
            kw.setdefault(ext_requests.URL_PARAM_START, ar.offset)
        if ar.limit is not None:
            kw.setdefault(ext_requests.URL_PARAM_LIMIT, ar.limit)
        if ar.order_by is not None:
            sc = ar.order_by[0]
            if sc.startswith('-'):
                sc = sc[1:]
                kw.setdefault(ext_requests.URL_PARAM_SORTDIR, 'DESC')
            kw.setdefault(ext_requests.URL_PARAM_SORT, sc)
        #~ print '20120901 TODO get_request_url'

        return self.plugin.build_plain_url(
            ar.actor.app_label, ar.actor.__name__, *args, **kw)

    def request_handler(self, ar, *args, **kw):
        return ''

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.action.label
        return label

    def action_call(self, request, bound_action, after_show):
        return "oops"
