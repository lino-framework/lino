# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Creates a welcome mail for all persons in the database.
"""


from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from lino.utils.instantiator import Instantiator
from lino.core.utils import resolve_model

from lino.api import rt


def objects():

    from lino.modlib.outbox.models import RecipientType
    Person = rt.modules.contacts.Person

    root = settings.SITE.user_model.objects.get(username='root')

    mail = Instantiator('outbox.Mail').build
    recipient_to = Instantiator(
        'outbox.Recipient', type=RecipientType.to).build

    for p in Person.objects.filter(email=''):
        try:
            p.first_name.encode('ascii')
            p.email = p.first_name.lower() + "@example.com"
            p.save()
        except UnicodeError:
            pass

    for person in Person.objects.exclude(email=''):
        m = mail(user=root, subject='Welcome %s!' % person.first_name)
        yield m
        yield recipient_to(mail=m, partner=person)
