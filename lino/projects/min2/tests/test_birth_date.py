# -*- coding: utf-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Test certain aspects of `birth_date`.

This module is part of the Lino test suite. You can test only this
module by issuing either::

  $ go min2
  $ python manage.py test tests.test_birth_date

or::

  $ go lino
  $ python setup.py test -s tests.ProjectsTests.test_min2


"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import rt

from lino.utils.xmlgen.html import E
from lino.utils.djangotest import RemoteAuthTestCase
from django.core.exceptions import ValidationError


def create(m, **kw):
    obj = m(**kw)
    obj.full_clean()
    obj.save()
    obj.after_ui_save(None, None)
    return obj


class QuickTest(RemoteAuthTestCase):

    fixtures = ['std', 'few_countries', 'few_cities']

    def test_this(self):

        Person = rt.modules.contacts.Person
        Link = rt.modules.humanlinks.Link
        LinkTypes = rt.modules.humanlinks.LinkTypes
        LinksByHuman = rt.modules.humanlinks.LinksByHuman

        father = create(
            Person, first_name="John", last_name="Doe",
            gender="M",
            birth_date='1980-07-31')
        try:
            son = create(
                Person, first_name="Joseph", last_name="Doe",
                gender="M",
                birth_date='2009-02-30')
        except ValidationError:
            pass
        else:
            self.fail("Expected ValidationError")
        son = create(
            Person, first_name="Joseph", last_name="Doe",
            gender="M",
            birth_date='2009-02-28')
        create(Link, parent=father, child=son, type=LinkTypes.parent)

        mary = create(
            Person, first_name="Mary", last_name="Doe",
            gender="F",
            birth_date='2010-01-30')
        create(Link, parent=father, child=mary, type=LinkTypes.parent)

        self.assertEqual(Person.objects.count(), 3)

        ar = LinksByHuman.request(father)
        s = ar.to_rst()
        # print(s)
        self.assertEqual(s, """\
John is
Father of *Mary* (4 years)
Father of *Joseph* (5 years)

Create relationship as **Father**/**Son** **Adoptive father**/**Adopted son** **Husband** **Partner** **Stepfather**/**Stepson** **Brother** **Cousin** **Uncle**/**Nephew** **Relative** **Other**
""")

        # Here we are just testing whether no exception is risen. The
        # ouptut itself is more thoroughly tested elsewhere.
        html = LinksByHuman.get_slave_summary(father, ar)
        s = E.tostring(html)
        self.assertEqual(s[:5], '<div>')
        

