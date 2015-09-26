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
  - PROTECT : system.SiteConfig.site_calendar, cal.Subscription.calendar
- cal.Event :
  - CASCADE : cal.Guest.event
- cal.EventType :
  - PROTECT : users.User.event_type, system.SiteConfig.default_event_type, cal.RecurrentEvent.event_type, cal.Event.event_type
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
  - CASCADE : contacts.Person.partner_ptr, contacts.Company.partner_ptr
  - PROTECT : users.User.partner, cal.Guest.partner
- contacts.Person :
  - PROTECT : contacts.Role.person
- contacts.RoleType :
  - PROTECT : contacts.Role.type
- contenttypes.ContentType :
  - PROTECT : gfks.HelpText.content_type, cal.Task.owner_type, cal.Event.owner_type
- countries.Country :
  - PROTECT : countries.Place.country, contacts.Partner.country
- countries.Place :
  - PROTECT : countries.Place.parent, contacts.Partner.city
- users.User :
  - PROTECT : users.Authority.user, cal.Subscription.user, cal.Task.user, cal.RecurrentEvent.user, cal.Event.user
<BLANKLINE>
