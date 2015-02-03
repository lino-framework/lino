What are choicelists?
=====================

A :class:`lino.core.choicelists.ChoiceList` is a "hard-coded" list of
translatable values.

In plain Django, whenever you use a `choices` attribute on a database
field, then you should consider using a choicelist instead.

..
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.docs.settings.demo'
    >>> from lino.api.doctests import *
    

For example the :class:`lino.modlib.system.mixins.Genders` choicelist.


Choicelists are actors. This means that they are globally accessible
using their actor name.

>>> print(rt.modules.system.Genders)
system.Genders

Choicelists are never instantiated. They are just the class object
itself.

>>> from lino.modlib.system.mixins import Genders
>>> Genders is rt.modules.system.Genders
True

Choicelists can be represented as tables:

>>> rt.show(Genders)
======= ======== ========
 value   name     text
------- -------- --------
 M       male     Male
 F       female   Female
======= ======== ========
<BLANKLINE>

Each row of a choicelist is a choice. Named choices are accessible as
class attributes on their choicelist:

>>> Genders.male
<Genders.male:M>

>>> Genders.female
<Genders.female:F>


A ChoiceList has an `objects` method (not attribute) which returns an
iterator over its choices:

>>> print(Genders.objects())
[<Genders.male:M>, <Genders.female:F>]

Each Choice has a "value", a "name" and a "text". 

The **value** is what gets stored when this choice is assigned to a
database field.

>>> [g.value for g in Genders.objects()]
[u'M', u'F']

The **name** is how Python code can refer to this choice.

>>> [g.name for g in Genders.objects()]
[u'male', u'female']

>>> print(repr(Genders.male))
<Genders.male:M>

The **text** is what the user sees.
It is a translatable string, 
implemented using Django's i18n machine:

>>> [g.text for g in Genders.objects()] # doctest: +ELLIPSIS
[<django.utils.functional.__proxy__ object at ...>, <django.utils.functional.__proxy__ object at ...>]

Calling `unicode` of a choice is (usually) the same as calling unicode
on its `text` attribute:

>>> [unicode(g) for g in Genders.objects()]
[u'Male', u'Female']
>>> [unicode(g.text) for g in Genders.objects()]
[u'Male', u'Female']


The text of a choice depends on the current user language.

>>> from django.utils import translation

>>> with translation.override('fr'):
...     [unicode(g) for g in Genders.objects()]
[u'Masculin', u'F\xe9minin']

>>> with translation.override('de'):
...     [unicode(g) for g in Genders.objects()]
[u'M\xe4nnlich', u'Weiblich']

>>> with translation.override('et'):
...     [unicode(g) for g in Genders.objects()]
[u'Mees', u'Naine']


