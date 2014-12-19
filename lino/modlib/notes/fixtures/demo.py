# coding: utf-8
# Copyright 2009-2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""Generate one houndred notes.

TODO: this fixture fails if `settings.SITE.project_model` is empty or
points to a model that has no `name` field.

"""

from django.conf import settings
from django.utils.translation import ugettext as _
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model
from lino.utils import Cycler


def objects():
    #~ User = settings.SITE.user_model()
    User = resolve_model(settings.SITE.user_model)
    Note = resolve_model('notes.Note')
    NoteType = resolve_model('notes.NoteType')

    USERS = Cycler(User.objects.all())
    if settings.SITE.project_model is not None:
        Project = resolve_model(settings.SITE.project_model)
        qs = Project.objects.all()
        if qs.count() > 10:
            qs = qs[:10]
        PROJECTS = Cycler(qs)
        #~ PROJECTS = Cycler(Project.objects.filter(name__startswith="A"))
        #~ PROJECTS = Cycler(Project.objects.all())
    #~ COMPANIES = Cycler(Company.objects.all())
    NTYPES = Cycler(NoteType.objects.all())

    #~ u = User.objects.get(username='root')

    notetype = Instantiator('notes.NoteType').build
    tel = notetype(name="phone report")
    yield tel
    yield notetype(name="todo")

    for i in range(100):
        kw = dict(user=USERS.pop(),
                  date=settings.SITE.demo_date(days=i),
                  subject="Important note %d" % i,
                  #~ company=COMPANIES.pop(),
                  type=NTYPES.pop())
        if settings.SITE.project_model is not None:
            kw.update(project=PROJECTS.pop())
        yield Note(**kw)
