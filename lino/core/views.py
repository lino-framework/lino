# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Utility functions used by :mod:`lino.modlib.extjs.views`.

"""

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django import http
from django.core import exceptions

from lino.core import constants
from lino.core import actors
from lino.utils.jsgen import py2js


def json_response_kw(**kw):
    return json_response(kw)


def json_response(x, content_type='application/json'):
    s = py2js(x)
    """
    Theroretically we should send content_type='application/json'
    (http://stackoverflow.com/questions/477816/the-right-json-content-type),
    but "File uploads are not performed using Ajax submission, 
    that is they are not performed using XMLHttpRequests. (...) 
    If the server is using JSON to send the return object, then 
    the Content-Type header must be set to "text/html" in order 
    to tell the browser to insert the text unchanged into the 
    document body." 
    (http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm)
    See 20120209.
    """
    return http.HttpResponse(s, content_type=content_type)
    #~ return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='application/json')
    #~ return HttpResponse(s, content_type='text/json')


def requested_actor(app_label, actor):
    """
    Utility function which returns the requested actor,
    either directly or (if specified name is a model) that
    model's default table.
    """
    x = getattr(settings.SITE.modules, app_label, None)
    if x is None:
        raise http.Http404("There's no app_label %r here" % app_label)
        # raise Exception("There's no app_label %r here" % app_label)
    cl = getattr(x, actor, None)
    if not isinstance(cl, type):
        raise http.Http404("%s.%s is not a class" % (app_label, actor))
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
        if not a.get_view_permission(user.profile):
            raise exceptions.PermissionDenied(
                "As %s you have no permission to run this action."
                % user.profile)
                # The text of an Exception may not be
                # internationalized because some error handling code
                # may want to write it to a plain ascii stream.
    ar = rpt.request(request=request, action=a, rqdata=rqdata, **kw)
    return ar

