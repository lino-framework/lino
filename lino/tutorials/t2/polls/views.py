from lino.tutorials.t2.polls.models import Poll
from django.http import HttpResponse

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    output = """<p><a href="lino/">lino</a> <a href="admin/">admin</a></p>"""
    output += "<ul>%s</ul>" % ', '.join(["<li>%s</li>" % p.question for p in latest_poll_list])
    return HttpResponse(output)