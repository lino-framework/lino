# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The `demo` fixture for `humanlinks`
===================================

Creates two fictive families:

- Hubert & Gaby Frisch-Frogemuth with their children and grand-children
- 

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.utils.instantiator import InstanceGenerator
from lino.api import dd, rt


def objects():

    Person = dd.resolve_model(dd.apps.humanlinks.person_model)
    Link = rt.modules.humanlinks.Link
    LinkTypes = rt.modules.humanlinks.LinkTypes
    ar = rt.login()

    households = dd.resolve_app('households')
    if households:
        married = households.Type.objects.get(
            **dd.str2kw('name', _("Married couple")))
        divorced = households.Type.objects.get(
            **dd.str2kw('name', _("Divorced couple")))

    ig = InstanceGenerator()
    ig.add_instantiator(
        'person', Person, 'first_name last_name gender birth_date')
    ig.add_instantiator(
        'link', Link, 'parent child type')

    NAME1 = "Frisch"

    opa = ig.person("Hubert", NAME1, 'M', '1933-07-21')
    oma = ig.person("Gaby", "Frogemuth", 'F', '1934-08-04')

    P = ig.person("Paul", NAME1, 'M', '1967-06-19')
    L = ig.person("Ludwig", NAME1, 'M', '1968-06-01')
    A = ig.person("Alice", NAME1, 'F', '1969-12-19')
    B = ig.person("Bernd", NAME1, 'M', '1971-09-10')

    P1 = ig.person("Paula", "Einzig", 'F', '1968-12-19')
    P1A = ig.person("Peter", NAME1, 'M', '1987-06-19')
    P2 = ig.person("Petra", "Zweith", 'F', '1968-12-19')
    P2A = ig.person("Philippe", NAME1, 'M', '1997-06-19')
    P2B = ig.person("Clara", NAME1, 'F', '1999-06-19')
    P3 = ig.person("Dora", "Drosson", 'F', '1971-12-19')
    P3A = ig.person("Dennis", NAME1, 'M', '2001-06-19')

    L1 = ig.person("Laura", "Loslever", 'F', '1968-04-27')
    L1A = ig.person("Melba", NAME1, 'F', '2002-04-05')
    L1B = ig.person("Irma", NAME1, 'F', '2008-03-24')

    yield ig.flush()

    ig.link(opa, oma, LinkTypes.spouse)

    for i in (P, L, A, B):
        ig.link(opa, i, LinkTypes.parent)
        ig.link(oma, i, LinkTypes.parent)

    ig.link(P, P1A, LinkTypes.parent)
    ig.link(P1, P1A, LinkTypes.parent)

    ig.link(P, P2A, LinkTypes.parent)
    ig.link(P2, P2A, LinkTypes.parent)

    ig.link(P, P2B, LinkTypes.parent)
    ig.link(P2, P2B, LinkTypes.parent)

    ig.link(P, P3A, LinkTypes.parent)
    ig.link(P3, P3A, LinkTypes.parent)

    ig.link(P, P2, LinkTypes.spouse)

    ig.link(L, L1, LinkTypes.spouse)

    for i in (L1A, L1B):
        ig.link(L, i, LinkTypes.parent)
        ig.link(L1, i, LinkTypes.parent)

    yield ig.flush()

    if households:
        households.Household.create_household(ar, opa, oma, married)

        households.Household.create_household(ar, P, P1, divorced)
        hh = households.Household.create_household(ar, P, P2, married)
        hh.members_by_role('head')[0].set_primary(ar)
        hh.members_by_role('partner')[0].set_primary(ar)

        households.Household.create_household(ar, L, L1, married)

    A = ig.person("Albert", "Adam", 'M', '1973-07-21')
    B = ig.person("Bruno", "Braun", 'M', '1973-07-22')

    E = ig.person("Eveline", "Evrard", 'F', '1974-08-21')
    F = ig.person("Françoise", "Freisen", 'F', '1974-08-22')

    I = ig.person("Ilja", "Adam", 'M', '1994-08-22')
    J = ig.person("Jan", "Braun", 'M', '1996-08-22')
    K = ig.person("Kevin", "Braun", 'M', '1998-08-22')
    L = ig.person("Lars", "Braun", 'M', '1998-08-22')

    M = ig.person("Monique", "Braun", 'F', '2000-08-22')
    N = ig.person("Noémie", "Adam", 'F', '2002-08-22')
    O = ig.person("Odette", "Adam", 'F', '2004-08-22')
    P = ig.person("Pascale", "Adam", 'F', '2004-08-22')

    yield ig.flush()

    ig.link(A, I, LinkTypes.parent)
    ig.link(A, N, LinkTypes.parent)
    ig.link(A, O, LinkTypes.parent)
    ig.link(A, P, LinkTypes.parent)

    ig.link(B, J, LinkTypes.parent)
    ig.link(B, K, LinkTypes.parent)
    ig.link(B, L, LinkTypes.parent)
    ig.link(B, M, LinkTypes.parent)

    ig.link(E, I, LinkTypes.parent)
    ig.link(E, J, LinkTypes.parent)
    ig.link(E, K, LinkTypes.parent)
    ig.link(E, L, LinkTypes.parent)

    ig.link(F, M, LinkTypes.parent)
    ig.link(F, N, LinkTypes.parent)
    ig.link(F, O, LinkTypes.parent)
    ig.link(F, P, LinkTypes.parent)

    ig.link(A, F, LinkTypes.spouse)
    ig.link(B, E, LinkTypes.spouse)

    yield ig.flush()

    if households:
        households.Household.create_household(ar, A, E, married)
        households.Household.create_household(ar, A, F, divorced)
        households.Household.create_household(ar, B, E, divorced)
        households.Household.create_household(ar, B, F, married)
