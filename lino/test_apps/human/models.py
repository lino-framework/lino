# -*- coding: utf-8 -*-
## Copyright 2008-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This test application explains some basic truths about humans.

The database structure used for the following examples is very simple,
we define a single model `Person` 
which just inherits :class:`lino.mixins.human.Human`:

.. code-block::

  from lino.mixins import Human

  class Person(Human):
      pass


Overview
---------

Lino is not complicated. Humans have three properties: 
`first_name`, `last_name` and `gender`.
All these fields may be blank, 
except if your application changed that rule, 
using :func:`lino.dd.update_field`.

The :class:`Genders <lino.mixins.human.Genders>` choicelist
defines the possible values for the `gender` field of a Human.

>>> from lino.mixins import Genders
>>> [g.value for g in Genders.objects()]
['M', 'F']
>>> [unicode(g) for g in Genders.objects()]
[u'Male', u'Female']

The default `__unicode__` method of a Human includes 
the "salutation" which indicates the gender:

>>> print Person(first_name="John", last_name="Smith",gender=Genders.male)
Mr John Smith

>>> print Person(last_name="Smith",gender=Genders.female)
Mrs Smith

If you don't 

>>> print Person(first_name="John", last_name="Smith")
John Smith

>>> print Person(first_name="John")
John


The salutation
--------------

The salutation depends not only on the gender, but also on the 
current language.

>>> p = Person(first_name="Jean",last_name="Dupont",gender=Genders.male)
>>> print p
Mr Jean Dupont

>>> from lino.utils import babel

>>> babel.set_language('fr')
>>> print p
M. Jean Dupont

>>> babel.set_language('de')
>>> print p
Herrn Jean Dupont

In German you may need to get a nominative form of the salutation:

>>> print p.get_full_name(nominative=True)
Herr Jean Dupont


You may want to omit the salutation.

>>> print p.get_full_name(salutation=False)
Jean Dupont



Uppercase last name
-------------------

In France it is usual to print the last name with captial letters.

>>> babel.set_language('fr')
>>> print p.get_full_name(upper=True)
M. Jean DUPONT

Lino also has a setting :attr:`lino.Lino.uppercase_last_name`
which causes this to be the default.

>>> from django.conf import settings
>>> settings.LINO.uppercase_last_name = True

>>> print p
M. Jean DUPONT

When setting :attr:`lino.Lino.uppercase_last_name` is set and you 
*don't* want uppercase last names, then you must specify it explicitly:

>>> print p.get_full_name(upper=False)
M. Jean Dupont


The `mf` method
---------------

The :meth:`mf <lino.mixins.humans.Human.mf>` method of a Human
is useful in document templates when you want to generate texts 
that differ depending on the gender of a Human.

>>> babel.set_language('en')
>>> mankind = [Person(first_name="Adam", gender=Genders.male),
...   Person(first_name="Eva", gender=Genders.female)]

>>> def about(p):
...     return "%s was the first %s." % (
...         p,p.mf("man","woman"))
>>> for p in mankind:
...     print about(p)
Mr Adam was the first man.
Mrs Eva was the first woman.


The `mf` method is a bit sexistic in that it returns 
the male value when the `gender` field is blank:

>>> p = Person(first_name="Kai")
>>> print p.mf("He","She")
He

Templates should use the third argument to handle this case properly:

>>> print p.mf("He","She","He or she")
He or she


"""

from lino.mixins import Human, Genders

class Person(Human):
    pass
