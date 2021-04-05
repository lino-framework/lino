# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.core import constants as ext_requests
from lino.core.renderer import HtmlRenderer
from lino.core.renderer import add_user_language

from .views import index_response

class Renderer(HtmlRenderer):

    """A  HTML render that uses Bootstrap3.

    """
    tableattrs = {
        'class': "table table-hover table-striped table-condensed"}
    cellattrs = dict(align="left", valign="top")

    can_auth = False

    def obj2url(self, ar, obj, **kw):
        ba = obj.get_detail_action(ar)
        if ba is not None:
            # no need to check again:
            # if ar is None or a.get_bound_action_permission(ar, obj, None):
            add_user_language(kw, ar)
            return self.get_detail_url(ar, ba.actor, obj.pk, **kw)

    # def get_detail_url(self, actor, pk, *args, **kw):
    #     return self.front_end.build_plain_url(
    #         actor.app_label,
    #         actor.__name__,
    #         str(pk), *args, **kw)

    # def pk2url(self, model, pk, **kw):
    #     """Overrides :meth:`lino.core.renderer.Renderer.pk2url`.
    #     """
    #     if pk is not None:
    #         return self.front_end.build_plain_url(
    #             model._meta.app_label, model.__name__, str(pk), **kw)

    def get_home_url(self, *args, **kw):
        return self.front_end.build_plain_url(*args, **kw)

    def get_request_url(self, ar, *args, **kw):
        if ar.actor.__name__ == "Main":
            return self.front_end.build_plain_url(*args, **kw)

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

        return self.front_end.build_plain_url(
            ar.actor.app_label, ar.actor.__name__, *args, **kw)

    def request_handler(self, ar, *args, **kw):
        return ''

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        return "%s" % label

    def action_call(self, ar, bound_action, status):
        a = bound_action.action
        if a.opens_a_window or (a.parameters and not a.no_params_window):
            return "#"
        sar = bound_action.request_from(ar)
        return self.get_request_url(sar)

    def render_action_response(self, ar):
        return index_response(ar)
