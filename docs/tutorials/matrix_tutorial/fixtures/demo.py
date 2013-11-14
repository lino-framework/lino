## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

from lino import dd
from django.conf import settings

from lino.utils import Cycler
#~ from lino.runtime import settings, matrix_tutorial

Entry = dd.resolve_model('matrix_tutorial.Entry')
EntryType = dd.resolve_model('matrix_tutorial.EntryType')
Company = dd.resolve_model('contacts.Company')

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def objects():
    
    yield EntryType(name="Consultation")
    yield EntryType(name="Evaluation")
    yield EntryType(name="Test")
    yield EntryType(name="Analysis")
    yield EntryType(name="Observation")
    
    TYPES = Cycler(EntryType.objects.all())
    COMPANIES = Cycler(Company.objects.all())
    USERS = Cycler(settings.SITE.user_model.objects.all())
    SUBJECTS = Cycler(LOREM_IPSUM.split())
    
    for i in range(200):
        d = settings.SITE.demo_date(-i)
        e = Entry(date=d,
            company=COMPANIES.pop(),
            user=USERS.pop(),
            subject=SUBJECTS.pop(),
            entry_type=TYPES.pop())
        if i % 7:
            yield e
    
