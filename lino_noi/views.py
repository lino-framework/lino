from django.http import HttpResponse
from django.views.generic import View

from lino.core.web import render_from_request


class TemplateView(View):
    template_name = 'detail.html'
    model = None
    

class Index(TemplateView):

    def get(self, request):
        s = render_from_request(request, self.template_name)
        return HttpResponse(s)


class Detail(TemplateView):

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        s = render_from_request(request, self.template_name, obj=obj)
        return HttpResponse(s)


def contacts(request, company_id):
    response = "You're looking at the contacts of company %s."
    return HttpResponse(response % company_id)

