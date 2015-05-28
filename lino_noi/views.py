from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

# from lino.core.web import render_from_request
from lino.core.utils import full_model_name
from lino.core.requests import BaseRequest


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
        obj = self.model.objects.get(pk=pk)
        s = render_from_request(request, self.template_name, obj=obj)
        return HttpResponse(s)


def render_from_request(request, template_name, **context):
    template = settings.SITE.jinja_env.get_template(template_name)
    ar = BaseRequest(
        renderer=settings.SITE.plugins.bootstrap3.renderer,
        request=request)
    context = ar.get_printable_context(**context)
    return template.render(**context)

# def contacts(request, company_id):
#     response = "You're looking at the contacts of company %s."
#     return HttpResponse(response % company_id)

