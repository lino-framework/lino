# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals
from builtins import str

import logging
logger = logging.getLogger(__name__)

from lino.core import constants as ext_requests
from lino.core.renderer import HtmlRenderer
from lino.core.renderer import add_user_language

# from lino.utils.memo import Parser


class Renderer(HtmlRenderer):

    """A  HTML render that uses Bootstrap3.

    """

    can_auth = False
    # is_interactive = True

    # def __init__(self, plugin):
    #     Renderer.__init__(self, plugin)
    #     for a in plugin.site.actors_list:
    #         a.get_handle()

    #     self.memo_parser = Parser()

    #     def url2html(parser, s):
    #         url, text = s.split(None, 1)
    #         if not text:
    #             text = url
    #         return '<a href="%s">%s</a>' % (url, text)

    #     self.memo_parser.register_command('url', url2html)

    def instance_handler(self, ar, obj, **kw):
        a = obj.get_detail_action(ar)
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar, obj, None):
                add_user_language(kw, ar)
                return self.get_detail_url(obj, **kw)

    def get_detail_url(self, obj, *args, **kw):
        return self.plugin.build_plain_url(
            obj._meta.app_label,
            obj.__class__.__name__,
            str(obj.pk), *args, **kw)

    def pk2url(self, ar, pk, **kw):
        if pk is not None:
            return self.plugin.build_plain_url(
                ar.actor.model._meta.app_label,
                ar.actor.model.__name__,
                str(pk), **kw)

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

    def action_call(self, request, bound_action, status):
        ar = bound_action.request()
        return self.get_request_url(ar)

    def js2url(self, js):
        """There is no Javascript here."""
        return js
