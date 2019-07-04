# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""

Summary from <http://en.wikipedia.org/wiki/Restful>: 

    On an element:

    - GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
    - PUT : Update the addressed member of the collection or create it with the specified ID. 
    - POST : Treats the addressed member as a collection and creates a new subordinate of it. 
    - DELETE : Delete the addressed member of the collection. 

    On a list:

    - GET : List the members of the collection. 
    - PUT : Replace the entire collection with another collection. 
    - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
      The ID created is included as part of the data returned by this operation. 
    - DELETE : Delete the entire collection.
    



"""
from builtins import str

import json

from os import environ

from django import http
from django.db import models
from django.conf import settings
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from lino.core import auth

from lino.core.signals import pre_ui_delete
from lino.core.utils import obj2unicode

# from etgen import html as xghtml
from etgen.html import E, tostring, Document

# E = xghtml.E

from lino.utils import ucsv
from lino.utils import isiterable
from lino.utils import dblogger

from lino.core import actions
from lino.core import fields

from lino.core.views import requested_actor, action_request
from lino.core.views import json_response, json_response_kw

from lino.core import constants
from lino.core.requests import BaseRequest, PhantomRow

MAX_ROW_COUNT = 300


class HttpResponseDeleted(http.HttpResponse):
    status_code = 204


def elem2rec_empty(ar, ah, elem, **rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    # ~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    # ~ rec = elem2rec1(ar,ah,elem)
    # ~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    # ~ rec.update(id=elem.pk) or -99999)
    if ar.actor.parameters:
        rec.update(
            param_values=ar.actor.params_layout.params_store.pv2dict(
                ar, ar.param_values))
    return rec


def delete_element(ar, elem):
    if elem is None:
        raise Warning("Cannot delete None")
    msg = ar.actor.disable_delete(elem, ar)
    if msg is not None:
        ar.error(None, msg, alert=True)
        return settings.SITE.kernel.default_renderer.render_action_response(ar)

    # ~ dblogger.log_deleted(ar.request,elem)

    # ~ changes.log_delete(ar.request,elem)

    pre_ui_delete.send(sender=elem, request=ar.request)

    try:
        elem.delete()
    except Exception as e:
        dblogger.exception(e)
        msg = _("Failed to delete %(record)s : %(error)s."
                ) % dict(record=obj2unicode(elem), error=e)
        # ~ msg = "Failed to delete %s." % element_name(elem)
        ar.error(None, msg)
        return settings.SITE.kernel.default_renderer.render_action_response(ar)
        # ~ raise Http404(msg)

    return HttpResponseDeleted()


@method_decorator(never_cache, name='dispatch')
class AdminIndex(View):
    """
    Similar to PlainIndex
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kw):
        # logger.info("20150427 AdminIndex.get()")
        # settings.SITE.startup()
        renderer = settings.SITE.plugins.extjs.renderer
        # if settings.SITE.user_model is not None:
        #     user = request.subst_user or request.user
        #     a = settings.SITE.get_main_action(user)
        #     if a is not None and a.get_view_permission(user.user_type):
        #         kw.update(on_ready=renderer.action_call(request, a, {}))
        return http.HttpResponse(renderer.html_page(request, **kw))

def test_version_mismatch(request):
    if not environ.get("PYCHARM_HOSTED", False) and request.GET.get(constants.URL_PARAM_LINO_VERSION) is not None and \
                       float(request.GET.get(constants.URL_PARAM_LINO_VERSION)) != settings.SITE.kernel.code_mtime:
        return dict(alert=_("Version mismatch"),
                    message=_("Your browser is using a previous version of the site, press OK to reload the site"),
                    alert_eval_js="window.location.reload(true);")
    else:
        return {}



class MainHtml(View):
    def get(self, request, *args, **kw):
        # ~ logger.info("20130719 MainHtml")
        settings.SITE.startup()
        ui = settings.SITE.kernel
        # ~ raise Exception("20131023")
        ar = BaseRequest(request)
        html = settings.SITE.get_main_html(
            request, extjs=settings.SITE.plugins.extjs)
        html = settings.SITE.plugins.extjs.renderer.html_text(html)
        ar.success(html=html)
        ar.set_response(**test_version_mismatch(request))
        return ui.default_renderer.render_action_response(ar)


class unused_Authenticate(View):
    """This view is being used when :setting:`remote_user_header` is
    empty (and :setting:`user_model` not).
    :class:`lino.core.auth.SessionUserMiddleware`

    """

    def get(self, request, *args, **kw):
        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME)
        if action_name == 'logout':
            username = request.session.pop('username', None)
            auth.logout(request)
            # request.session.pop('password', None)
            # ~ username = request.session['username']
            # ~ del request.session['password']

            ar = BaseRequest(request)
            ar.success("User %r logged out." % username)
            return ar.renderer.render_action_response(ar)
        raise http.Http404()

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kw):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            request, username=username, password=password)
        if user is not None:
            # user.is_authenticated:
            auth.login(request, user)

        ar = BaseRequest(request)
        # mw = auth.get_auth_middleware()
        # msg = mw.authenticate(username, password, request)
        # if msg:
        #     request.session.pop('username', None)
        #     ar.error(msg)
        # else:
        #     request.session['username'] = username
        #     # request.session['password'] = password
        # ar.success(("Now logged in as %r" % username))
        #     # print "20150428 Now logged in as %r (%s)" % (username, user)
        if user is None:
            ar.error(_("Failed to log in as {}.".format(username)))
        else:
            ar.success(("Now logged in as %r" % username))
        return ar.renderer.render_action_response(ar)


class RunJasmine(View):
    """
    """

    def get(self, request, *args, **kw):
        ui = settings.SITE.kernel
        return http.HttpResponse(
            ui.extjs_renderer.html_page(request, run_jasmine=True))


class EidAppletService(View):
    """
    """

    def post(self, request, *args, **kw):
        ui = settings.SITE.kernel
        return ui.success(html='Hallo?')


class Callbacks(View):
    def get(self, request, thread_id, button_id):
        return settings.SITE.kernel.run_callback(request, thread_id, button_id)


def choices_for_field(ar, holder, field):
    """
    Return the choices for the given field and the given HTTP request
    whose `holder` is either a Model, an Actor or an Action.
    """
    if not holder.get_view_permission(ar.request.user.user_type):
        raise Exception(
            "{user} has no permission for {holder}".format(
                user=ar.request.user, holder=holder))
    # model = holder.get_chooser_model()
    chooser = holder.get_chooser_for_field(field.name)
    # logger.info('20140822 choices_for_field(%s.%s) --> %s',
    #             holder, field.name, chooser)
    if chooser:
        qs = chooser.get_request_choices(ar, holder)
        if not isiterable(qs):
            raise Exception("%s.%s_choices() returned non-iterable %r" % (
                holder.model, field.name, qs))
        if chooser.simple_values:
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                d[constants.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar.request, field)
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:  # values are (value, text) tuples
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
                return d
        return (qs, row2dict)

    if field.choices:
        qs = field.choices

        def row2dict(obj, d):
            if type(obj) is list or type(obj) is tuple:
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
            else:
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar.request, field)
                d[constants.CHOICES_VALUE_FIELD] = str(obj)
            return d

        return (qs, row2dict)

    if isinstance(field, fields.VirtualField):
        field = field.return_type

    if isinstance(field, fields.RemoteField):
        field = field.field

    if isinstance(field, models.ForeignKey):
        m = field.remote_field.model
        t = m.get_default_table()
        qs = t.request(request=ar.request).data_iterator

        # logger.info('20120710 choices_view(FK) %s --> %s', t, qs.query)

        def row2dict(obj, d):
            d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                obj, ar.request, field)
            d[constants.CHOICES_VALUE_FIELD] = obj.pk
            return d
    else:
        raise http.Http404("No choices for %s" % field)
    return (qs, row2dict)


def choices_response(actor, request, qs, row2dict, emptyValue):
    """
    :param actor: requesting Actor
    :param request: web request
    :param qs: list of django model QS,
    :param row2dict: function for converting data set into a dict for json
    :param emptyValue: The Text value to represent None in the choice-list
    :return: json web responce

    Filters data-set acording to quickseach
    Counts total rows in the set,
    Calculates offset and limit
    Adds None value
    returns
    """
    quick_search = request.GET.get(constants.URL_PARAM_FILTER, None)
    offset = request.GET.get(constants.URL_PARAM_START, None)
    limit = request.GET.get(constants.URL_PARAM_LIMIT, None)
    if isinstance(qs, models.QuerySet):
        qs = qs.filter(qs.model.quick_search_filter(quick_search)) if quick_search else qs
        count = qs.count()

        if offset:
            qs = qs[int(offset):]
            # ~ kw.update(offset=int(offset))

        if limit:
            # ~ kw.update(limit=int(limit))
            qs = qs[:int(limit)]

        rows = [row2dict(row, {}) for row in qs]

    else:
        rows = [row2dict(row, {}) for row in qs]
        if quick_search:
            txt = quick_search.lower()

            rows = [row for row in rows
                    if txt in row[constants.CHOICES_TEXT_FIELD].lower()]
        count = len(rows)
        rows = rows[int(offset):] if offset else rows
        rows = rows[:int(limit)] if limit else rows

    # Add None choice
    if emptyValue is not None and not quick_search:
        empty = dict()
        empty[constants.CHOICES_TEXT_FIELD] = emptyValue
        empty[constants.CHOICES_VALUE_FIELD] = None
        rows.insert(0, empty)

    return json_response_kw(count=count, rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)


class ActionParamChoices(View):
    # Examples: `welfare.pcsw.CreateCoachingVisit`
    def get(self, request, app_label=None, actor=None, an=None, field=None, **kw):
        actor = requested_actor(app_label, actor)
        ba = actor.get_url_action(an)
        if ba is None:
            raise Exception("Unknown action %r for %s" % (an, actor))
        field = ba.action.get_param_elem(field)
        qs, row2dict = choices_for_field(ba.request(request=request), ba.action, field)
        if field.blank:
            emptyValue = '<br/>'
        else:
            emptyValue = None
        return choices_response(actor, request, qs, row2dict, emptyValue)


class Choices(View):
    def get(self, request, app_label=None, rptname=None, fldname=None, **kw):
        """If `fldname` is specified, return a JSON object with two
        attributes `count` and `rows`, where `rows` is a list of
        `(display_text, value)` tuples.  Used by ComboBoxes or similar
        widgets.

        If `fldname` is not specified, returns the choices for the
        `record_selector` widget.

        """
        rpt = requested_actor(app_label, rptname)
        emptyValue = None
        if fldname is None:
            ar = rpt.request(request=request)
            # ~ rh = rpt.get_handle(self)
            # ~ ar = ViewReportRequest(request,rh,rpt.default_action)
            # ~ ar = dbtables.TableRequest(self,rpt,request,rpt.default_action)
            # ~ rh = ar.ah
            # ~ qs = ar.get_data_iterator()
            qs = ar.data_iterator

            # ~ qs = rpt.request(self).get_queryset()

            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                # getattr(obj,'pk')
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:
            # NOTE: if you define a *parameter* with the same name as
            # some existing *data element* name, then the parameter
            # will override the data element here in choices view.
            field = rpt.get_param_elem(fldname)
            if field is None:
                field = rpt.get_data_elem(fldname)
            if field.blank:
                # logger.info("views.Choices: %r is blank",field)
                emptyValue = '<br/>'
            qs, row2dict = choices_for_field(rpt.request(request=request), rpt, field)

        return choices_response(rpt, request, qs, row2dict, emptyValue)


class Restful(View):
    """
    Used to collaborate with a restful Ext.data.Store.
    """

    @method_decorator(csrf_protect)
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

    @method_decorator(csrf_protect)
    def delete(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)
        ar.set_selected_pks(pk)
        return delete_element(ar, ar.selected_rows[0])

    def get(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        assert pk is None, 20120814
        ar = rpt.request(request=request)
        rh = ar.ah
        rows = [
            rh.store.row2dict(ar, row, rh.store.list_fields)
            for row in ar.sliced_data_iterator]
        kw = dict(count=ar.get_total_count(), rows=rows)
        kw.update(title=str(ar.get_title()))
        return json_response(kw)

    @method_decorator(csrf_protect)
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


NOT_FOUND = "%s has no row with primary key %r"


class ApiElement(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, app_label=None, actor=None, pk=None):
        ui = settings.SITE.kernel
        rpt = requested_actor(app_label, actor)
        # if not rpt.get_view_permission(request.user.user_type):
        #     raise PermissionDenied("{} has permission to view {}".format(
        #         request.user.user_type, rpt))
        # print(rpt, request.user.user_type)

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
            # print(
            #     "20170116 views.ApiElement.get", ba,
            #     ar.action_param_values)
            elem = ar.selected_rows[0]
        else:
            ar = ba.request(request=request)
            elem = None

        ar.renderer = ui.extjs_renderer
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
                datarec.update(test_version_mismatch(request))
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

        # if isinstance(ba.action, actions.RedirectAction):
        #     target = ba.action.get_target_url(elem)
        #     if target is None:
        #         raise http.Http404("%s failed for %r" % (ba, elem))
        #     return http.HttpResponseRedirect(target)

        if pk == '-99998':
            assert elem is None
            elem = ar.create_instance()
            ar.selected_rows = [elem]
        elif elem is None:
            raise http.Http404(NOT_FOUND % (rpt, pk))

        return settings.SITE.kernel.run_action(ar)

    @method_decorator(csrf_protect)
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

    @method_decorator(csrf_protect)
    def put(self, request, app_label=None, actor=None, pk=None):
        data = http.QueryDict(request.body)  # raw_post_data before Django 1.4
        # print("20180712 ApiElement.put() %s" % data)
        ar = action_request(
            app_label, actor, request, data, False,
            renderer=settings.SITE.kernel.extjs_renderer)
        ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    @method_decorator(csrf_protect)
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
    @method_decorator(csrf_protect)
    def post(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.POST, True)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        response = settings.SITE.kernel.run_action(ar)
        if request.POST.get('_document_domain', None) and response['Content-Type'] == "text/html":
            # Have same-origin policy work for iframe of file upload. see ticket #2885
            # https://stackoverflow.com/questions/22627392/extjs-fileuplaod-cross-origin-frame
            response.content= """<html><head><script type="text/javascript">document.domain="{}";</script></head><body>{}</body></html>""".format(
                    request.POST["_document_domain"],response.content.decode("utf-8") )
        return response

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        rh = ar.ah

        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT,
            ar.bound_action.action.default_format)
        # print(20170921, fmt)

        if fmt == constants.URL_FORMAT_JSON:
            rows = [rh.store.row2list(ar, row)
                    for row in ar.sliced_data_iterator]
            total_count = ar.get_total_count()
            # raise Exception("20171208 {}".format(ar.data_iterator.query))
            for row in ar.create_phantom_rows():
                if ar.limit is None or len(rows) + 1 < ar.limit or ar.limit == total_count + 1:
                    d = rh.store.row2list(ar, row)
                    rows.append(d)
                total_count += 1

            kw = dict(count=total_count,
                      rows=rows,
                      success=True,
                      no_data_text=ar.no_data_text)

            if True:
                kw.update(title=str(ar.get_title()))
            else:
                # 20190704 work in progress.
                # add open_in_own_window button after title of slave panel
                kw.update(title=str(ar.get_title()) + " " + tostring(ar.open_in_own_window_button()))

            if ar.actor.parameters:
                kw.update(
                    param_values=ar.actor.params_layout.params_store.pv2dict(
                        ar, ar.param_values))
            kw.update(test_version_mismatch(request))
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
            doc = Document(force_text(ar.get_title()))
            doc.body.append(E.h1(doc.title))
            t = doc.add_table()
            # ~ settings.SITE.kernel.ar2html(ar,t,ar.data_iterator)
            ar.dump2html(t, ar.data_iterator)
            doc.write(response, encoding='utf-8')
            return response

        return settings.SITE.kernel.run_action(ar)


class GridConfig(View):

    @method_decorator(csrf_protect)
    def put(self, request, app_label=None, actor=None):
        rpt = requested_actor(app_label, actor)
        PUT = http.QueryDict(request.body)  # raw_post_data before Django 1.4
        gc = dict(
            widths=[int(x)
                    for x in PUT.getlist(constants.URL_PARAM_WIDTHS)],
            columns=[str(x)
                     for x in PUT.getlist(constants.URL_PARAM_COLUMNS)],
            hiddens=[(x == 'true')
                     for x in PUT.getlist(constants.URL_PARAM_HIDDENS)],
            # ~ hidden_cols=[str(x) for x in PUT.getlist('hidden_cols')],
        )

        filter = PUT.get('filter', None)
        if filter is not None:
            filter = json.loads(filter)
            gc['filters'] = [constants.dict2kw(flt) for flt in filter]

        name = PUT.get('name', None)
        if name is None:
            name = constants.DEFAULT_GC_NAME
        else:
            name = int(name)

        gc.update(label=PUT.get('label', "Standard"))
        try:
            msg = rpt.save_grid_config(name, gc)
        except IOError as e:
            msg = _("Error while saving GC for %(table)s: %(error)s") % dict(
                table=rpt, error=e)
            return settings.SITE.kernel.error(None, msg, alert=True)
        # ~ logger.info(msg)
        settings.SITE.kernel.extjs_renderer.build_site_cache(True)
        return settings.SITE.kernel.success(msg)
