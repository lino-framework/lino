# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Views for `lino.modlib.tinymce`.

"""
from builtins import str

import logging
logger = logging.getLogger(__name__)

from django import http
from django.conf import settings
from django.views.generic import View

from lino.utils.jsgen import py2js
from lino.core.views import requested_actor


from jinja2 import Template as JinjaTemplate

from lino.api import dd, rt


class Templates(View):

    """
    Called by TinyMCE (`template_external_list_url
    <http://www.tinymce.com/wiki.php/configuration:external_template_list_url>`_)
    to fill the list of available templates.

    """

    def get(self, request,
            app_label=None, actor=None,
            pk=None, fldname=None, tplname=None, **kw):

        if request.method == 'GET':

            rpt = requested_actor(app_label, actor)
            elem = rpt.get_row_by_pk(None, pk)
            if elem is None:
                raise http.Http404("%s %s does not exist." % (rpt, pk))

            TextFieldTemplate = rt.modules.tinymce.TextFieldTemplate
            if tplname:
                tft = TextFieldTemplate.objects.get(pk=int(tplname))
                if settings.SITE.trusted_templates:
                    #~ return http.HttpResponse(tft.text)
                    template = JinjaTemplate(tft.text)
                    context = dict(request=request,
                                   instance=elem, **rt.modules)
                    return http.HttpResponse(template.render(**context))
                else:
                    return http.HttpResponse(tft.text)

            qs = TextFieldTemplate.objects.all().order_by('name')

            templates = []
            for obj in qs:
                url = dd.plugins.tinymce.build_plain_url(
                    'templates',
                    app_label, actor, pk, fldname, str(obj.pk))
                templates.append([
                    str(obj.name), url, str(obj.description)])
            js = "var tinyMCETemplateList = %s;" % py2js(templates)
            return http.HttpResponse(js, content_type='text/json')
        raise http.Http404("Method %r not supported" % request.method)

