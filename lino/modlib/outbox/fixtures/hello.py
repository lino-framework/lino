# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)


#~ from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from lino.utils.instantiator import Instantiator, i2d
from lino.core.dbutils import resolve_model


#~ from lino.modlib.properties import models as properties

def objects():

    from lino.modlib.outbox.models import RecipientType
    Person = resolve_model("contacts.Person")
    Company = resolve_model("contacts.Company")

    User = resolve_model(settings.SITE.user_model)
    root = User.objects.get(username='root')

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
    #~ for person in Person.objects.filter(email__isnull=False):
        m = mail(user=root, subject='Welcome %s!' % person.first_name)
        yield m
        yield recipient_to(mail=m, partner=person)
            #~ address=person.email,name=person.get_full_name(salutation=False))
    #~ m = mail(user=root,subject='Hello %s!' % root.first_name)
    #~ yield m
    #~ yield recipient_to(mail=m,partner=root)
