# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)



from lino.utils.instantiator import Instantiator, i2d
from django.utils.translation import ugettext_lazy as _

from lino.api import dd


def objects():

    #~ slot = Instantiator('courses.Slot','name start_time end_time').build
    #~
    #~ kw = dict(monday=True,tuesday=True,wednesday=False,thursday=True,friday=True)
    #~ yield slot("Erste Stunde","16:00","17:00",**kw)
    #~ yield slot("Zweite Stunde","17:00","18:00",**kw)
    #~ yield slot("Dritte Stunde","18:00","19:00",**kw)
    #~
    #~ kw = dict(wednesday=True)
    #~ yield slot("Mittwochs 13 Uhr","13:00","14:00",**kw)
    #~ yield slot("Mittwochs 14 Uhr","14:00","15:00",**kw)
    #~ yield slot("Mittwochs 15 Uhr","15:00","16:00",**kw)
    #~ yield slot("Mittwochs 16 Uhr","16:00","17:00",**kw)
    #~ yield slot("Mittwochs 17 Uhr","17:00","18:00",**kw)
    #~ yield slot("Mittwochs 18 Uhr","18:00","19:00",**kw)

    courses = dd.resolve_app('courses')

    yield courses.Line(**dd.babelkw('name',
                                 de=u"Deutsch Anfänger",
                                 fr=u"Allemand débutants",
                                 en=u"German beginners",
                                 ))
    yield courses.Line(**dd.babelkw('name',
                                 de=u"Französisch Anfänger",
                                 fr=u"Français débutants",
                                 en=u"French beginners",
                                 ))
