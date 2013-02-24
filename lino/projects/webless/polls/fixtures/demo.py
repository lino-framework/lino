from django.conf import settings
from django.utils import timezone

from lino import dd

Poll = dd.resolve_model('polls.Poll')
Choice = dd.resolve_model('polls.Choice')

DATA = """
What is your preferred colour? | Blue | Red | Yellow | other
Do you like Django? | Yes | No | Not yet decided
Do you like ExtJS? | Yes | No | Not yet decided
"""

def objects():
    for ln in DATA.splitlines():
        if ln:
            a = ln.split('|')
            p = Poll(question=a[0].strip(),pub_date=timezone.now())
            yield p
            for choice in a[1:]:
                yield Choice(choice_text=choice.strip(),poll=p,votes=0)
                
    #~ from django.contrib.auth.models import User
    yield settings.LINO.modules.auth.User.objects.create_superuser('root', 'root@example.com', '1234')
