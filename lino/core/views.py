# Copyright 2010-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Utility functions used by :mod:`lino.modlib.extjs.views`.

"""

from django.conf import settings
from django.db import models
from django import http
from django.core import exceptions

from lino.core import constants
from lino.core import actors
from lino.utils.jsgen import py2js
from lino.api import _


def json_response_kw(**kw):
    return json_response(kw)


def json_response(x, content_type='application/json', status=200):
    if True:
        s = py2js(x)
    else:
        try:
            s = py2js(x)
        except Exception as e:
            raise Exception("Failed to render {!r} : {}".format(x, e))

    # Theroretically we should send content_type='application/json'
    # (http://stackoverflow.com/questions/477816/the-right-json-content-type),
    # but "File uploads are not performed using Ajax submission, that
    # is they are not performed using XMLHttpRequests. (...)  If the
    # server is using JSON to send the return object, then the
    # Content-Type header must be set to "text/html" in order to tell
    # the browser to insert the text unchanged into the document
    # body."
    # (http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm)
    # See 20120209.

    return http.HttpResponse(s, content_type=content_type, status=status)
    #~ return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='application/json')
    #~ return HttpResponse(s, content_type='text/json')


def requested_actor(app_label, actor):
    """Return the requested actor, either directly or (if specified name
    is a model) that model's default table.

    """
    x = settings.SITE.models.get(app_label)
    # x = getattr(settings.SITE.models, app_label, None)
    if x is None:
        raise http.Http404("There's no app_label %r here" % app_label)
        # raise Exception("There's no app_label %r here" % app_label)
    cl = getattr(x, actor, None)
    if not isinstance(cl, type):
        raise http.Http404("%s.%s is not a class" % (app_label, actor))
        # raise http.Http404("%s.%s is not a class (but %r)" % (
        #     app_label, actor, cl))
    if issubclass(cl, models.Model):
        return cl.get_default_table()
    if not issubclass(cl, actors.Actor):
        #~ raise http.Http404("%r is not an actor" % cl)
        raise http.Http404("%r is not an actor" % cl)
    return cl


def action_request(app_label, actor, request, rqdata, is_list, **kw):
    # print(20160329, rqdata.keys())
    rpt = requested_actor(app_label, actor)
    action_name = rqdata.get(constants.URL_PARAM_ACTION_NAME, None)
    if not action_name:
        if is_list:
            action_name = rpt.default_list_action_name
        else:
            action_name = rpt.default_elem_action_name
    a = rpt.get_url_action(action_name)
    if a is None:
        raise http.Http404(
            "%s has no url action %r (possible values are %s)" % (
                rpt, action_name, rpt.get_url_action_names()))
    user = request.subst_user or request.user
    if True:  # False:  # 20130829
        if not a.get_view_permission(user.user_type):
            # print("20200110 {} {}".format(a.required, user.user_type.role.__class__))
            raise exceptions.PermissionDenied(
                "As %s you have no view permission for this action."
                % user.user_type)
                # The text of an Exception may not be
                # internationalized because some error handling code
                # may want to write it to a plain ascii stream.
    ar = rpt.request(request=request, action=a, rqdata=rqdata, **kw)
    # print("20200901", ar, rqdata)
    return ar


def choices_response(actor, request, qs, row2dict, emptyValue, field=None):
    """
    :param actor: requesting Actor
    :param request: web request
    :param qs: list of django model QS,
    :param row2dict: function for converting data set into a dict for json
    :param emptyValue: The Text value to represent None in the choice-list
    :param is_blank_value: The Text value to represent filtering rows that are blank in PV the choice-list
    :param is_not_blank_value: The Text value to represent filtering rows that are not blank in PV the choice-list

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
    wt = request.GET.get(constants.URL_PARAM_WINDOW_TYPE, None)

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

    if wt == constants.WINDOW_TYPE_PARAMS and field and field.blank:
        rows.insert(0, {
            # constants.CHOICES_TEXT_FIELD: actor.get_blank_filter_text(),
            constants.CHOICES_TEXT_FIELD: _("Blank"),
            constants.CHOICES_VALUE_FIELD: constants.CHOICES_BLANK_FILTER_VALUE
        })
        rows.insert(1, {
            # constants.CHOICES_TEXT_FIELD: actor.get_not_blank_filter_text(),
            constants.CHOICES_TEXT_FIELD: _("Not Blank"),
            constants.CHOICES_VALUE_FIELD: constants.CHOICES_NOT_BLANK_FILTER_VALUE
        })

    # Add None choice
    if emptyValue is not None and not quick_search:
        empty = dict()
        empty[constants.CHOICES_TEXT_FIELD] = emptyValue
        empty[constants.CHOICES_VALUE_FIELD] = None
        rows.insert(0, empty)

    return json_response_kw(count=count, rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
