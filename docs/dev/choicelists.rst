===========================
Introduction to choicelists
===========================

.. To run only this test:

   $ python setup.py test -s tests.DocsTests.test_choicelists

A :class:`ChoiceList <lino.core.choicelists.ChoiceList>` is a
"constant"[#constant]_ ordered list of translatable values.

Wherever in a *plain Django* application you use a `choices` attribute
on a database field, in a *Lino* application you should consider using
a :class:`ChoiceList <lino.core.choicelists.ChoiceList>` instead.

..
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...     'lino.projects.min1.settings.doctests'
    >>> from lino.api.doctest import *
    

For example the :mod:`lino.projects.min1` we have the following choicelists:


>>> from lino.core.choicelists import choicelist_choices
>>> for value, text in choicelist_choices():
...     print "%s : %s" % (value, unicode(text))
cal.AccessClasses : AccessClasses
cal.DurationUnits : DurationUnits
cal.EventEvents : Observed events
cal.EventStates : Event states
cal.GuestStates : Guest states
cal.Recurrencies : Recurrencies
cal.TaskStates : Task states
cal.Weekdays : Weekdays
countries.PlaceTypes : PlaceTypes
lino.BuildMethods : BuildMethods
plausibility.Checkers : Plausibility checkers
system.Genders : Genders
system.PeriodEvents : Observed events
system.YesNo : Yes or no
users.UserGroups : User Groups
users.UserLevels : User Levels
users.UserProfiles : User Profiles

ChoiceLists are actors, and choiceLists are tables. 
This means that they are globally accessible
in :data:`rt.modules` using their plugin name (aka "app label") and
actor name. 

For example: the :class:`Genders <lino.modlib.system.mixins.Genders>`
choicelist is in a plugin called "system":

>>> rt.show(rt.modules.system.Genders)
======= ======== ========
 value   name     text
------- -------- --------
 M       male     Male
 F       female   Female
======= ======== ========
<BLANKLINE>

The text of a choice is a **translatable** string, while *value* and
*name* remain **unchanged**:

>>> with translation.override('de'):
...     rt.show(rt.modules.system.Genders)
====== ======== ==========
 Wert   name     Text
------ -------- ----------
 M      male     Männlich
 F      female   Weiblich
====== ======== ==========
<BLANKLINE>


Like every Actor, ChoiceLists are **never instantiated**. They are
just the class object itself:

>>> from lino.modlib.system.mixins import Genders
>>> Genders is rt.modules.system.Genders
True


Each row of a choicelist is a choice. Individual choices can have a
name, which makes them accessible as **class attributes on their
choicelist**:

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

The **text** is what the user sees.  It is a translatable string,
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



Comparing Choices uses their *value* (not the *name* nor *text*):

>>> UserLevels = rt.modules.users.UserLevels

>>> UserLevels.manager > UserLevels.user
True
>>> UserLevels.manager == '40'
True
>>> UserLevels.manager == 'manager'
False
>>> UserLevels.manager == ''
False





.. rubric:: Footnotes

.. [#constant] We put "constant" between quotation marks because of course it may
  vary. But if it does so, then only once at server startup.



