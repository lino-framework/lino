.. _lino.tutorial.human:

============
About Humans
============

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_human

This document explains some basic things about humans (as the
:mod:`lino.mixins.human` module sees them).

.. contents::
   :depth: 1
   :local:


The database structure used for the following examples is very simple:

.. literalinclude:: models.py

That is, we define a single model `Person` which just inherits
:class:`lino.mixins.human.Human`.


.. 
  >>> from __future__ import print_function 
  >>> from human.models import Person
  >>> from lino.modlib.system.choicelists import Genders
  >>> from django.utils import translation


Database fields
---------------

The `Human` mixin defines four database fields: `first_name`,
`middle_name`, `last_name` and `gender`.

The `gender` field is a pointer to
the :class:`lino.modlib.system.choicelists.Genders` choicelist.

All these fields may be blank (except if your application changed that
rule using :func:`lino.core.inject.update_field`).


Parsing names
-------------

>>> from lino.mixins.human import name2kw

Examples:

>>> name2kw("Saffre Luc")
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rilke Rainer Maria")
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Van Rompuy Herman")
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("'T Jampens Jan")
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Van den Bossche Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}
>>> name2kw("Den Tandt Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Den Tandt'}

In more complicated cases, a comma is required to help:

>>> name2kw("Mombanga born Ngungi, Maria Magdalena")
{'first_name': 'Maria Magdalena', 'last_name': 'Mombanga born Ngungi'}

Some examples with `first_name` first:

>>> name2kw("Luc Saffre", False)
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rainer Maria Rilke", False)
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Herman Van Rompuy", False)
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("Jan 'T Jampens",False)
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Marc Antoine Bernard Van den Bossche", False)
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}
>>> name2kw("Marc Antoine Bernard Den Tandt", False)
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Den Tandt'}

Edge cases:

>>> name2kw("")
{}

Bibliography:

#. http://en.wikipedia.org/wiki/Dutch_name
#. http://www.myheritage.com/support-post-130501/dutch-belgium-german-french-surnames-with-prefix-such-as-van



Examples:

>>> from lino.mixins.human import parse_name

>>> print(parse_name("luc saffre"))
{'first_name': 'Luc', 'last_name': 'Saffre'}

But careful with name prefixes:

>>> print(parse_name("herman van veen"))
{'first_name': 'Herman', 'last_name': 'van veen'}
>>> print(parse_name("jean van den bossche"))
{'first_name': 'Jean', 'last_name': 'van den bossche'}

>>> parse_name("Foo")
Traceback (most recent call last):
...
ValidationError: [u'Cannot find first and last name in "Foo"']






Salutation
----------

The default `__unicode__` method of a Human includes 
the "salutation" which indicates the gender:

>>> print(Person(first_name="John", last_name="Smith", gender=Genders.male))
Mr John Smith

>>> print(Person(last_name="Smith", gender=Genders.female))
Mrs Smith

If you don't specify a gender, Lino doesn't print any salutation:

>>> print(Person(first_name="John", last_name="Smith"))
John Smith

>>> print(Person(first_name="John"))
John

The salutation depends not only on the gender, but also on the 
current language.
This is Mr Jean Dupont:

>>> p = Person(first_name="Jean",last_name="Dupont",gender=Genders.male)

We can address him in English:

>>> print(p)
Mr Jean Dupont

The same object will render differently when we switch to French...

>>> with translation.override('fr'):
...     print(p)
M. Jean Dupont

... or to German...

>>> with translation.override('de'):
...     print(p)
Herr Jean Dupont



The full name
-------------

Calling `unicode` on a person actually returns the same as the property `full_name`:

>>> print(p)
Mr Jean Dupont

>>> print(p.full_name)
Mr Jean Dupont

They are equivalent *here*, but remember that applications may override 
one of them (usually `__unicode__`) because in reality not all humans 
are equal. 

>>> print(p.get_full_name())
Mr Jean Dupont

The :func:`get_full_name <lino.mixins.human.Human.get_full_name>` 
function has 2 optional parameters `nominative` and `salutation`.

In German you may need to get a nominative form of the salutation:

>>> with translation.override('de'):
...     print(p.get_full_name())
Herrn Jean Dupont

>>> with translation.override('de'):
...     print(p.get_full_name(nominative=True))
Herr Jean Dupont

You may want to omit the salutation:

>>> with translation.override('de'):
...     print(p.get_full_name(salutation=False))
Jean Dupont

The property `full_name` (without parentheses) of Person 
is an alias for the function call `get_full_name()` without parameters.

>>> with translation.override('de'):
...    print(p.full_name)
Herrn Jean Dupont





Uppercase last name
-------------------

In France it is usual to print the last name with captial letters.

>>> with translation.override('fr'): 
...    print(p.get_full_name(upper=True))
M. Jean DUPONT

Lino also has a setting :setting:`uppercase_last_name` which causes
this to be the default.

>>> from django.conf import settings
>>> settings.SITE.uppercase_last_name = True

>>> with translation.override('fr'):
...     print(p)
M. Jean DUPONT

When :setting:`uppercase_last_name` is set to True and you
(exceptionally) do *not* want uppercase last names, then you must
specify it explicitly:

>>> with translation.override('fr'):
...    print(p.get_full_name(upper=False))
M. Jean Dupont


The title of a human
--------------------

The :attr:`title <lino.mixins.human.Human.title>` field of a human is
for specifying a `title
<https://en.wikipedia.org/wiki/Title>`__ such as "Dr." or "PhD".

>>> settings.SITE.uppercase_last_name = False
>>> p.title = "Dr."
>>> p.save()
>>> print(p.get_full_name())
Mr Dr. Jean Dupont
>>> with translation.override('de'):
...     print(p.get_full_name())
Herrn Dr. Jean Dupont



The `mf` method
---------------

The :meth:`mf <lino.mixins.human.Human.mf>` method of a Human
is useful in document templates when you want to generate texts 
that differ depending on the gender of a Human.

>>> mankind = [Person(first_name="Adam", gender=Genders.male),
...   Person(first_name="Eva", gender=Genders.female)]

>>> def about(p):
...     return "%s was the first %s." % (
...         p,p.mf("man","woman"))
>>> for p in mankind:
...     print(about(p))
Mr Adam was the first man.
Mrs Eva was the first woman.


The `mf` method is a bit sexistic in that it returns the male value
when the `gender` field is blank:

>>> p = Person(first_name="Conchita", last_name="Wurst")
>>> print(p.mf("He","She"))
He

Templates can use the third argument to handle this case properly:

>>> print(p.mf("He", "She", "He or she"))
He or she


We'll reuse the same files for another little lesson
about :ref:`lino.tutorial.pisa`.


The `strip_name_prefix` function
--------------------------------

>>> from lino.mixins.human import strip_name_prefix
>>> strip_name_prefix("Vandenberg")
'VANDENBERG'

>>> strip_name_prefix("Van den Berg")
'BERG'

>>> strip_name_prefix("Vonnegut")
'VONNEGUT'

>>> strip_name_prefix("von Goethe")
'GOETHE'

>>> strip_name_prefix("Jean")
'JEAN'

>>> strip_name_prefix("Jean-Jacques")
'JEAN-JACQUES'

>>> strip_name_prefix("Nemard")
'NEMARD'

