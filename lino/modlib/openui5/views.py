# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Views for `lino.modlib.bootstrap3`.

"""
from __future__ import division
from past.utils import old_div

import logging
logger = logging.getLogger(__name__)

from django import http
from django.conf import settings
from django.views.generic import View
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
# from django.contrib import auth
from lino.core import auth


# from lino.api import dd
from lino.core import constants
# from lino.core import auth
from lino.core.requests import BaseRequest
from lino.core.tablerequest import TableRequest
import json

from lino.core.views import requested_actor, action_request
from lino.core.views import json_response, json_response_kw

from lino.core.views import action_request
from lino.core.utils import navinfo
from etgen.html import E
from etgen import html as xghtml

from lino.api import rt
import re

# Taken from lino.modlib.extjs.views
NOT_FOUND = "%s has no row with primary key %r"
def elem2rec_empty(ar, ah, elem, **rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    #~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    #~ rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    #~ rec.update(id=elem.pk) or -99999)
    if ar.actor.parameters:
        rec.update(
            param_values=ar.actor.params_layout.params_store.pv2dict(
                ar, ar.param_values))
    return rec


class ApiElement(View):

    def get(self, request, app_label=None, actor=None, pk=None):
        ui = settings.SITE.kernel
        rpt = requested_actor(app_label, actor)

        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME,
                                      rpt.default_elem_action_name)
        ba = rpt.get_url_action(action_name)
        if ba is None:
            raise http.Http404("%s has no action %r" % (rpt, action_name))

        if pk and pk != '-99999' and pk != '-99998':
            # ~ ar = ba.request(request=request,selected_pks=[pk])
            # ~ print 20131004, ba.actor
            # Use url selected rows as selected PKs if defined, otherwise use the PK defined in the url path
            sr = request.GET.getlist(constants.URL_PARAM_SELECTED)
            if not sr:
                sr = [pk]
            ar = ba.request(request=request, selected_pks=sr)
            elem = ar.selected_rows[0]
        else:
            ar = ba.request(request=request)
            elem = None

        ar.renderer = ui.default_renderer
        ah = ar.ah

        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT, ba.action.default_format)

        if ba.action.opens_a_window:

            if fmt == constants.URL_FORMAT_JSON:
                if pk == '-99999':
                    elem = ar.create_instance()
                    datarec = ar.elem2rec_insert(ah, elem)
                elif pk == '-99998':
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar, ah, elem)
                elif elem is None:
                    datarec = dict(
                        success=False, message=NOT_FOUND % (rpt, pk))
                else:
                    datarec = ar.elem2rec_detailed(elem)
                return json_response(datarec)

            after_show = ar.get_status(record_id=pk)
            tab = request.GET.get(constants.URL_PARAM_TAB, None)
            if tab is not None:
                tab = int(tab)
                after_show.update(active_tab=tab)

            return http.HttpResponse(
                ui.extjs_renderer.html_page(
                    request, ba.action.label,
                    on_ready=ui.extjs_renderer.action_call(
                        request, ba, after_show)))

        if isinstance(ba.action, actions.RedirectAction):
            target = ba.action.get_target_url(elem)
            if target is None:
                raise http.Http404("%s failed for %r" % (ba, elem))
            return http.HttpResponseRedirect(target)

        if pk == '-99998':
            assert elem is None
            elem = ar.create_instance()
            ar.selected_rows = [elem]
        elif elem is None:
            raise http.Http404(NOT_FOUND % (rpt, pk))
        return settings.SITE.kernel.run_action(ar)

    def post(self, request, app_label=None, actor=None, pk=None):
        ar = action_request(
            app_label, actor, request, request.POST, True,
            renderer=settings.SITE.kernel.extjs_renderer)
        if pk == '-99998':
            elem = ar.create_instance()
            ar.selected_rows = [elem]
        else:
            ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def put(self, request, app_label=None, actor=None, pk=None):
        data = http.QueryDict(request.body)  # raw_post_data before Django 1.4
        # logger.info("20150130 %s", data)
        ar = action_request(
            app_label, actor, request, data, False,
            renderer=settings.SITE.kernel.extjs_renderer)
        ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def delete(self, request, app_label=None, actor=None, pk=None):
        data = http.QueryDict(request.body)
        ar = action_request(
            app_label, actor, request, data, False,
            renderer=settings.SITE.kernel.extjs_renderer)
        ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def old_delete(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)
        ar.set_selected_pks(pk)
        elem = ar.selected_rows[0]
        return delete_element(ar, elem)


class ApiList(View):


    def post(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.POST, True)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        return settings.SITE.kernel.run_action(ar)

    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        # Add this hack to support the 'sort' param which is different in Extjs6.
        if ar.order_by and ar.order_by[0]:
            _sort = ast.literal_eval(ar.order_by[0])
            sort = _sort[0]['property']
            if _sort[0]['direction'] and _sort[0]['direction'] == 'DESC':
                sort = '-' + sort
            ar.order_by = [str(sort)]
        ar.renderer = settings.SITE.kernel.default_renderer
        rh = ar.ah

        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT,
            ar.bound_action.action.default_format)

        if fmt == constants.URL_FORMAT_JSON:
            rows = [rh.store.row2list(ar, row)
                    for row in ar.sliced_data_iterator]
            total_count = ar.get_total_count()
            for row in ar.create_phantom_rows():
                if ar.limit is None or len(rows) + 1 < ar.limit or ar.limit == total_count + 1:
                    d = rh.store.row2list(ar, row)
                    rows.append(d)
                total_count += 1
            # assert len(rows) <= ar.limit
            kw = dict(count=total_count,
                      rows=rows,
                      success=True,
                      no_data_text=ar.no_data_text,
                      title=str(ar.get_title()))
            if ar.actor.parameters:
                kw.update(
                    param_values=ar.actor.params_layout.params_store.pv2dict(
                        ar, ar.param_values))
            return json_response(kw)

        if fmt == constants.URL_FORMAT_HTML:
            after_show = ar.get_status()

            sp = request.GET.get(
                constants.URL_PARAM_SHOW_PARAMS_PANEL, None)
            if sp is not None:
                # ~ after_show.update(show_params_panel=sp)
                after_show.update(
                    show_params_panel=constants.parse_boolean(sp))

            # if isinstance(ar.bound_action.action, actions.ShowInsert):
            #     elem = ar.create_instance()
            #     rec = ar.elem2rec_insert(rh, elem)
            #     after_show.update(data_record=rec)

            kw = dict(on_ready=
            ar.renderer.action_call(
                ar.request,
                ar.bound_action, after_show))
            # ~ print '20110714 on_ready', params
            kw.update(title=ar.get_title())
            return http.HttpResponse(ar.renderer.html_page(request, **kw))

        if fmt == 'csv':
            # ~ response = HttpResponse(mimetype='text/csv')
            charset = settings.SITE.csv_params.get('encoding', 'utf-8')
            response = http.HttpResponse(
                content_type='text/csv;charset="%s"' % charset)
            if False:
                response['Content-Disposition'] = \
                    'attachment; filename="%s.csv"' % ar.actor
            else:
                # ~ response = HttpResponse(content_type='application/csv')
                response['Content-Disposition'] = \
                    'inline; filename="%s.csv"' % ar.actor

            # ~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
            w = ucsv.UnicodeWriter(response, **settings.SITE.csv_params)
            w.writerow(ar.ah.store.column_names())
            if True:  # 20130418 : also column headers, not only internal names
                column_names = None
                fields, headers, cellwidths = ar.get_field_info(column_names)
                w.writerow(headers)

            for row in ar.data_iterator:
                w.writerow([str(v) for v in rh.store.row2list(ar, row)])
            return response

        if fmt == constants.URL_FORMAT_PRINTER:
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") %
                                MAX_ROW_COUNT)
            response = http.HttpResponse(
                content_type='text/html;charset="utf-8"')
            doc = xghtml.Document(force_text(ar.get_title()))
            doc.body.append(E.h1(doc.title))
            t = doc.add_table()
            # ~ settings.SITE.kernel.ar2html(ar,t,ar.data_iterator)
            ar.dump2html(t, ar.data_iterator)
            doc.write(response, encoding='utf-8')
            return response

        return settings.SITE.kernel.run_action(ar)

class Choices(View):
    pass

class Restful(View):

    """
    Used to collaborate with a restful Ext.data.Store.
    """

    def post(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)

        instance = ar.create_instance()
        # store uploaded files.
        # html forms cannot send files with PUT or GET, only with POST
        if ar.actor.handle_uploaded_files is not None:
            ar.actor.handle_uploaded_files(instance, request)

        data = request.POST.get('rows')
        data = json.loads(data)
        ar.form2obj_and_save(data, instance, True)

        # Ext.ensible needs list_fields, not detail_fields
        ar.set_response(
            rows=[ar.ah.store.row2dict(
                ar, instance, ar.ah.store.list_fields)])
        return json_response(ar.response)

    # def delete(self, request, app_label=None, actor=None, pk=None):
    #     rpt = requested_actor(app_label, actor)
    #     ar = rpt.request(request=request)
    #     ar.set_selected_pks(pk)
    #     return delete_element(ar, ar.selected_rows[0])

    def get(self, request, app_label=None, actor=None, pk=None):
        """
        Works, but is ugly to get list and detail
        """
        rpt = requested_actor(app_label, actor)


        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME,
                                      rpt.default_elem_action_name)
        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT,constants.URL_FORMAT_JSON)
        sr = request.GET.getlist(constants.URL_PARAM_SELECTED)
        if not sr:
            sr = [pk]
        ar = rpt.request(request=request, selected_pks=sr)
        if pk is None:
            rh = ar.ah
            rows = [
                rh.store.row2dict(ar, row, rh.store.all_fields)
                for row in ar.sliced_data_iterator]
            kw = dict(count=ar.get_total_count(), rows=rows)
            kw.update(title=str(ar.get_title()))
            return json_response(kw)

        else: #action_name=="detail": #ba.action.opens_a_window:

            ba = rpt.get_url_action(action_name)
            ah = ar.ah
            ar = ba.request(request=request, selected_pks=sr)
            elem = ar.selected_rows[0]
            if fmt == constants.URL_FORMAT_JSON:
                if pk == '-99999':
                    elem = ar.create_instance()
                    datarec = ar.elem2rec_insert(ah, elem)
                elif pk == '-99998':
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar, ah, elem)
                elif elem is None:
                    datarec = dict(
                        success=False, message=NOT_FOUND % (rpt, pk))
                else:
                    datarec = ar.elem2rec_detailed(elem)
                return json_response(datarec)


    def put(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)
        ar.set_selected_pks(pk)
        elem = ar.selected_rows[0]
        rh = ar.ah

        data = http.QueryDict(request.body).get('rows')
        data = json.loads(data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(request=request, action=a)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        ar.form2obj_and_save(data, elem, False)
        # Ext.ensible needs list_fields, not detail_fields
        ar.set_response(
            rows=[rh.store.row2dict(ar, elem, rh.store.list_fields)])
        return json_response(ar.response)


def http_response(ar, tplname, context):
    "Deserves a docstring"
    u = ar.get_user()
    lang = get_language()
    k = (u.user_type, lang)
    context = ar.get_printable_context(**context)
    context['ar'] = ar
    context['memo'] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    template = env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


def XML_response(ar, tplname, context):
    """
    Respone used for rendering XML views in openui5.
    Includes some helper functions for rendering.
    """
    # u = ar.get_user()
    # lang = get_language()
    # k = (u.user_type, lang)
    context = ar.get_printable_context(**context)
    # context['ar'] = ar
    # context['memo'] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    template = env.get_template(tplname)

    def bind(*args):
        """Helper function to wrap a string in {}s"""
        args = [str(a) for a in args]
        return "{" + "".join(args) + "}"

    context.update(bind=bind)

    def p(*args):
        """Debugger helper; prints out all args put into the filter but doesn't include them in the template.
        usage: {{debug | p}}
        """
        print(args)
        return ""

    env.filters.update(p=p)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


def layout2html(ar, elem):

    wl = ar.bound_action.get_window_layout()
    #~ print 20120901, wl.main
    lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)

    items = list(lh.main.as_plain_html(ar, elem))
    # if navigator:
    #     items.insert(0, navigator)
    #~ print E.tostring(E.div())
    #~ if len(items) == 0: return ""
    return E.form(*items)


class Tickets(View):
    """
    Was a static View for Tickets,
    IS currently main app entry point,
    """
    def get(self, request, app_label="tickets", actor="AllTickets"):
        ar = action_request(app_label, actor, request, request.GET, True)
        ar.renderer = settings.SITE.plugins.openui5.renderer

        # ui = settings.SITE.plugins.openui5
        # main = settings.SITE.get_main_html(ar.request, extjs=ui)
        # main = ui.renderer.html_text(main)
        # print(main)
        context = dict(
            title=ar.get_title(),
            heading=ar.get_title(),
            # main=main,
        )

        context.update(ar=ar)

        context = ar.get_printable_context(**context)
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template("openui5/tickets_ui5.html")

        return http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')

class MainHtml(View):
    def get(self, request, *args, **kw):
        """Returns a json struct for the main user dashboard."""
        #~ logger.info("20130719 MainHtml")
        settings.SITE.startup()
        #~ raise Exception("20131023")
        ar = BaseRequest(request)
        html = settings.SITE.get_main_html(
            request, extjs=settings.SITE.plugins.openui5)
        html = settings.SITE.plugins.openui5.renderer.html_text(html)
        ar.success(html=html)
        return json_response(ar.response, ar.content_type)

class Connector(View):
    """
    Static View for Tickets,
    Uses a template for generating the XML views  rather then layouts
    """
    def get(self, request, name=None):
        # ar = action_request(None, None, request, request.GET, True)
        ar = BaseRequest(
            # user=user,
            request=request,
            renderer=settings.SITE.plugins.openui5.renderer)
        u = ar.get_user()

        context = dict(
            menu=settings.SITE.get_site_menu(None, u.user_type)
        )

        print(u)
        print name
        if name.startswith("view/"):
            tplname = "openui5/" + name

        elif name.startswith("dialog/SignInActionFormPanel"):
            tplname = "openui5/fragment/SignInActionFormPanel.fragment.xml"

        elif name.startswith("menu/user/user.fragment.xml"):
            tplname = "openui5/fragment/UserMenu.fragment.xml"

        elif name.startswith("menu/"):
            tplname = "openui5/fragment/Menu.fragment.xml"
            sel_menu = name.split("/",1)[1].split('.',1)[0]
            # [05/Feb/2018 09:32:25] "GET /ui/menu/mailbox.fragment.xml HTTP/1.1" 200 325
            for i in context['menu'].items:
                if i.name == sel_menu:
                    context.update(dict(
                        opened_menu=i
                    ))
                    break
            else:
                raise Exception("No Menu with name %s"%sel_menu)
        elif name.startswith("grid/") or name.startswith("slavetable/"): # Table/grid view
            # todo Get table data
            # "grid/tickets/AllTickets.view.xml"
            # or
            # "slavetable/tickets/AllTickets.view.xml
            app_label, actor = re.match(r"(?:grid|slavetable)\/(.+)\/(.+).view.xml$", name).groups()
            ar = action_request(app_label, actor, request, request.GET, True)
            actor = rt.models.resolve(app_label + "." + actor)
            print(ar.ah.store.pk_index) # indexk of PK
            context.update({
                "actor": actor,
                "columns": actor.get_handle().get_columns(),
                "actions": actor.get_actions(),
                "title": actor.label,

            })
            if name.startswith("slavetable/"):
                tplname = "openui5/view/slaveTable.view.xml"
            else:
                tplname = "openui5/view/table.view.xml" # Change to "grid" to match action?
            # ar = action_request(app_label, actor, request, request.GET, True)
            # add to context

        elif name.startswith("detail"):  # Detail view
            # "detail/tickets/AllTickets.view.xml"
            app_label, actor = re.match(r"detail\/(.+)\/(.+).view.xml$", name).groups()
            actor = rt.models.resolve(app_label + "." + actor)
            # detail_action = actor.actions['detail']
            detail_action = actor.detail_action
            window_layout = detail_action.get_window_layout()
            layout_handle = window_layout.get_layout_handle(settings.SITE.plugins.openui5)
            layout_handle.main.elements # elems # Refactor into actor get method?
            context.update({
                "actor": actor,
                # "columns": actor.get_handle().get_columns(),
                "actions": actor.get_actions(),
                "title": actor.label, #
                # "main_elems": layout_handle.main.elements,
                "main": layout_handle.main,
                "layout_handle": layout_handle

            })
            tplname = "openui5/view/detail.view.xml"  # Change to "grid" to match action?
            # ar = action_request(app_label, actor, request, request.GET, True)
            # add to context

        else:
            raise Exception("Can't find a view for path: {}".format(name))

        return XML_response(ar, tplname, context)



class Authenticate(View):
    def get(self, request, *args, **kw):
        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME)
        if action_name == 'logout':
            username = request.session.pop('username', None)
            auth.logout(request)
            # request.user = settings.SITE.user_model.get_anonymous_user()
            # request.session.pop('password', None)
            #~ username = request.session['username']
            #~ del request.session['password']
            target = '/'
            return http.HttpResponseRedirect(target)


            # ar = BaseRequest(request)
            # ar.success("User %r logged out." % username)
            # return ar.renderer.render_action_response(ar)
        raise http.Http404()

    def post(self, request, *args, **kw):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            request, username=username, password=password)
        auth.login(request, user, backend=u'lino.core.auth.backends.ModelBackend')
        target = '/'
        return http.HttpResponseRedirect(target)
        # ar = BaseRequest(request)
        # mw = auth.get_auth_middleware()
        # msg = mw.authenticate(username, password, request)
        # if msg:
        #     request.session.pop('username', None)
        #     ar.error(msg)
        # else:
        #     request.session['username'] = username
        #     # request.session['password'] = password
        #     # ar.user = request....
        #     ar.success(("Now logged in as %r" % username))
        #     # print "20150428 Now logged in as %r (%s)" % (username, user)
        # return ar.renderer.render_action_response(ar)

# Todo repalce with Tickets
class Index(View):
    """
    Render the main page.
    """
    def get(self, request, *args, **kw):
        # raise Exception("20171122 {} {}".format(
        #     get_language(), settings.MIDDLEWARE_CLASSES))
        ui = settings.SITE.plugins.bootstrap3
        # print("20170607", request.user)
        # assert ui.renderer is not None
        ar = BaseRequest(
            # user=user,
            request=request,
            renderer=ui.renderer)
        return index_response(ar)


def index_response(ar):
    ui = settings.SITE.plugins.openui5

    main = settings.SITE.get_main_html(ar.request, extjs=ui)
    main = ui.renderer.html_text(main)
    context = dict(
        title=settings.SITE.title,
        main=main,
    )
    # if settings.SITE.user_model is None:
    #     user = auth.AnonymousUser.instance()
    # else:
    #     user = request.subst_user or request.user
    # context.update(ar=ar)
    return http_response(ar, 'bootstrap3/index.html', context)
