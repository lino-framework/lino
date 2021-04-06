from django.conf import settings
from django.views.generic import View
from lino.core.views import json_response

class Suggestions(View):
    def get(self, request):
        suggesters = settings.SITE.plugins.memo.parser.suggesters
        trigger = request.GET.get("trigger")
        query = request.GET.get("query")
        return json_response(
            {"suggestions": list(suggesters[trigger].get_suggestions(query))}
        )
