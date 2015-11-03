.. _lino.tested.ddh:

=============================
Preventing accidental deletes
=============================

This document tests this functionality.


.. to run only this test:

    $ python setup.py test -s tests.DocsTests.test_ddh
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings.doctests'
    >>> from lino.api.doctest import *


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())  #doctest: +REPORT_UDIFF
- cal.Calendar :
  - PROTECT : cal.Subscription.calendar, system.SiteConfig.site_calendar
- cal.Event :
  - CASCADE : cal.Guest.event
- cal.EventType :
  - PROTECT : cal.Event.event_type, cal.RecurrentEvent.event_type, system.SiteConfig.default_event_type, users.User.event_type
- cal.GuestRole :
  - PROTECT : cal.Guest.role
- cal.Priority :
  - PROTECT : cal.Event.priority
- cal.Room :
  - PROTECT : cal.Event.room
- contacts.Company :
  - PROTECT : contacts.Role.company, system.SiteConfig.site_company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Company.partner_ptr, contacts.Person.partner_ptr
  - PROTECT : cal.Guest.partner, users.User.partner
- contacts.Person :
  - PROTECT : contacts.Role.person
- contacts.RoleType :
  - PROTECT : contacts.Role.type
- contenttypes.ContentType :
  - PROTECT : cal.Event.owner_type, cal.Task.owner_type, gfks.HelpText.content_type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, countries.Place.parent
- users.User :
  - PROTECT : cal.Event.user, cal.RecurrentEvent.user, cal.Subscription.user, cal.Task.user, users.Authority.user
<BLANKLINE>
