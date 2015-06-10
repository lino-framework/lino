# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds demo data for `households`

Creates some households by marrying a few Persons.

Every third household gets divorced: we put an `end_date` to that
membership and create another membership for the same person with
another person.

"""

from lino.core.utils import resolve_model


from lino.utils import Cycler
from lino.utils import i2d
from lino.api import dd, rt


def objects():

    Member = rt.modules.households.Member
    MemberRoles = rt.modules.households.MemberRoles
    # Household = resolve_model('households.Household')
    Person = resolve_model(dd.plugins.households.person_model)
    Type = resolve_model('households.Type')

    MEN = Cycler(Person.objects.filter(gender=dd.Genders.male)
                 .order_by('-id'))
    WOMEN = Cycler(Person.objects.filter(gender=dd.Genders.female)
                   .order_by('-id'))
    TYPES = Cycler(Type.objects.all())

    ses = rt.login()
    for i in range(5):
        pv = dict(
            head=MEN.pop(), partner=WOMEN.pop(),
            type=TYPES.pop())
        ses.run(
            Person.create_household,
            action_param_values=pv)
        # yield ses.response['data_record']
        # he = MEN.pop()
        # she = WOMEN.pop()
        
        # fam = Household(name=he.last_name + "-" + she.last_name, type_id=3)
        # yield fam
        # yield Member(household=fam, person=he, role=Role.objects.get(pk=1))
        # yield Member(household=fam, person=she, role=Role.objects.get(pk=2))

    i = 0
    for m in Member.objects.filter(role=MemberRoles.head):
        i += 1
        if i % 3 == 0:
            m.end_date = i2d(20020304)
            yield m

            pv = dict(
                head=m.person, partner=WOMEN.pop(),
                type=TYPES.pop())
            ses.run(
                Person.create_household,
                action_param_values=pv)
