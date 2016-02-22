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
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.docs.settings.doctests'
    >>> from lino.api.doctest import *


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())  #doctest: +REPORT_UDIFF
- concepts.Concept :
  - PROTECT : concepts.Link.parent
- contacts.Company :
  - PROTECT : contacts.Role.company, system.SiteConfig.site_company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Company.partner_ptr, contacts.Person.partner_ptr
  - PROTECT : users.User.partner
- contacts.Person :
  - PROTECT : contacts.Role.person
- contacts.RoleType :
  - PROTECT : contacts.Role.type
- contenttypes.ContentType :
  - PROTECT : changes.Change.object_type, gfks.HelpText.content_type, notifier.Notification.owner_type, uploads.Upload.owner_type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, countries.Place.parent
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : changes.Change.user, notifier.Notification.user, tinymce.TextFieldTemplate.user, uploads.Upload.user, users.Authority.user
<BLANKLINE>
