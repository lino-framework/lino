.. _lino.specs.holidays:

=================
Defining holidays
=================


.. How to test just this document

   $ python setup.py test -s tests.SpecsTests.test_holidays

Some initialization:

>>> from lino import startup
>>> startup('lino.projects.min2.settings.demo')
>>> from lino.api.doctest import *
>>> settings.SITE.verbose_client_info_message = True
>>> from lino.api import rt, _
>>> from atelier.utils import i2d
>>> RecurrentEvent = cal.RecurrentEvent
>>> Recurrencies = cal.Recurrencies


Recurrent event rules
=====================

Here are the standard holidays, defined as recurrent event rules
:class:`RecurrentEvent <lino.modlib.cal.models.RecurrentEvent>` by
:mod:`lino.modlib.cal.fixtures.std`:

>>> rt.show(cal.RecurrentEvents)
============ ========== ============================ ======================== ==================== =====================
 Start date   End Date   Designation                  Designation (et)         Recurrency           Calendar Event Type
------------ ---------- ---------------------------- ------------------------ -------------------- ---------------------
 1/1/13                  New Year's Day               Uusaasta                 yearly               Holidays
 2/11/13                 Rosenmontag                  Rosenmontag              Relative to Easter   Holidays
 2/13/13                 Ash Wednesday                Ash Wednesday            Relative to Easter   Holidays
 3/29/13                 Good Friday                  Good Friday              Relative to Easter   Holidays
 3/31/13                 Easter sunday                Easter sunday            Relative to Easter   Holidays
 4/1/13                  Easter monday                Easter monday            Relative to Easter   Holidays
 5/1/13                  International Workers' Day   kevadpüha                yearly               Holidays
 5/9/13                  Ascension of Jesus           Ascension of Jesus       Relative to Easter   Holidays
 5/20/13                 Pentecost                    Pentecost                Relative to Easter   Holidays
 7/1/13       8/31/13    Summer holidays              Suvevaheaeg              yearly               Holidays
 7/21/13                 National Day                 Belgia riigipüha         yearly               Holidays
 8/15/13                 Assumption of Mary           Assumption of Mary       yearly               Holidays
 10/31/13                All Souls' Day               All Souls' Day           yearly               Holidays
 11/1/13                 All Saints' Day              All Saints' Day          yearly               Holidays
 11/11/13                Armistice with Germany       Armistice with Germany   yearly               Holidays
 12/25/13                Christmas                    Esimene Jõulupüha        yearly               Holidays
============ ========== ============================ ======================== ==================== =====================
<BLANKLINE>


Relative to Easter
==================

Certain yearly events don't have a fixed day of the year but move
together with the Easter day.  They are also known as `moveable feasts
<https://en.wikipedia.org/wiki/Moveable_feast_%28observance_practice%29>`_.

Let's look at one of them, Ash Wednesday::

>>> ash = RecurrentEvent.objects.get(name="Ash Wednesday")

.. the following doesn't yet work:

    >>> # screenshot(ash, 'ash.png')

    followed by a .. image:: ash.png directive.


The :mod:`lino.modlib.cal.fixtures.std` fixture generates
automatically all Ash Wednesdays for a range of years:

>>> rt.show(cal.EventsByController, master_instance=ash)
============= =============== ===============
 When          Summary         Workflow
------------- --------------- ---------------
 Wed 2/13/13   Ash Wednesday   **Suggested**
 Wed 3/5/14    Ash Wednesday   **Suggested**
 Wed 2/18/15   Ash Wednesday   **Suggested**
 Wed 2/10/16   Ash Wednesday   **Suggested**
 Wed 3/1/17    Ash Wednesday   **Suggested**
 Wed 2/14/18   Ash Wednesday   **Suggested**
 Wed 3/6/19    Ash Wednesday   **Suggested**
============= =============== ===============
<BLANKLINE>


That range of years depends on some configuration variables:

- :attr:`ignore_dates_before <lino.modlib.cal.Plugin.ignore_dates_before>`
- :attr:`ignore_dates_after <lino.modlib.cal.Plugin.ignore_dates_after>`
- :attr:`lino.modlib.system.SiteConfig.max_auto_events`
- :attr:`the_demo_date <lino.core.site.Site.the_demo_date>`

>>> dd.plugins.cal.ignore_dates_before
>>> dd.plugins.cal.ignore_dates_after
datetime.date(2019, 10, 23)
>>> settings.SITE.site_config.max_auto_events
72
>>> settings.SITE.the_demo_date
datetime.date(2014, 10, 23)

Manually creating moving feasts
===============================

Event rules for moving feasts have their :attr:`every_unit
<lino.modlib.cal.models.RecurrentEvent.every_unit>` field set to
:attr:`easter <lino.modlib.cal.choicelists.Recurrencies.easter>`.

Lino then computes the offset (number of days) your :attr:`start_date`
and the easter date of the start year, and generates subsequent events
by moving their date so that the offset remains the same.

Lino uses the `easter()
<https://labix.org/python-dateutil#head-8863c4fc47132b106fcb00b9153e3ac0ab486a0d>`_
function of `dateutil` for getting the Easter date.

>>> from dateutil.easter import easter
>>> easter(2015)
datetime.date(2015, 4, 5)



Adding a local moving feast
===========================

.. verify that no events have actually been saved:
   >>> cal.Event.objects.count()
   132

We can add our own local custom holidays which depend on easter.

We create a *recurrent event rule* for it, specifying :attr:`easter
<lino.modlib.cal.choicelists.Recurrencies.easter>`.  in their
:attr:`every_unit <lino.modlib.cal.models.RecurrentEvent.every_unit>`
field.

>>> holidays = cal.EventType.objects.get(**dd.str2kw('name', _("Holidays")))
>>> obj = RecurrentEvent(name="Karneval in Kettenis",
...     every_unit=Recurrencies.easter,
...     start_date=i2d(20160209), event_type=holidays)
>>> obj.full_clean()
>>> obj.find_start_date(i2d(20160209))
datetime.date(2016, 2, 9)

>>> ar = rt.login()
>>> wanted = obj.get_wanted_auto_events(ar)
>>> len(wanted)
4
>>> print(ar.response['info_message'])
Generating events between 2016-02-09 and 2019-10-23.
Reached upper date limit 2019-10-23

>>> wanted[1]
Event(owner_type=26,start_date=2016-02-09,summary='Karneval in Kettenis',auto_type=1,event_type=1,state=<EventStates.suggested:10>)

.. verify that no events have actually been saved:
   >>> cal.Event.objects.count()
   132
