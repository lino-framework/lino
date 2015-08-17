# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Views for the public web interface of Lino Noi.

"""

from django.http import HttpResponse, Http404
from django.views.generic import View

from lino.core.utils import full_model_name
from lino.core.requests import BaseRequest
from lino.api import dd


def render_from_request(request, template_name, **context):
    template = dd.plugins.jinja.renderer.jinja_env.get_template(template_name)
    ar = BaseRequest(
        renderer=dd.plugins.noi.renderer,
        request=request)
    context = ar.get_printable_context(**context)
    return template.render(**context)


class TemplateView(View):
    template_name = 'detail.html'
    # model = None
    

class Index(TemplateView):

    template_name = 'noi/index.html'

    def get(self, request):
        s = render_from_request(request, self.template_name)
        return HttpResponse(s)


class Detail(TemplateView):

    model = None  # to be specified in views.py
    # template_name = 'noi/detail.html'

    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.template_name = "noi/{0}.html".format(full_model_name(model))
        super(TemplateView, self).__init__(*args, **kwargs)

    def get(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404()
        s = render_from_request(request, self.template_name, obj=obj)
        return HttpResponse(s)


