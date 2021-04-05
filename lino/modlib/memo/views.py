from django.conf import settings
from django.views.generic import View

class Suggestions(View):
    def get(self, request):
        suggesters = settings.SITE.plugins.memo.parser.suggesters
        trigger = request.GET.get("trigger")
        query = request.GET.get("query")
        return json_response(
            {"suggestions": list(suggesters[mention_char].get_suggestions(query))}
        )
