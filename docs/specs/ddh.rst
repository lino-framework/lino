.. _noi.specs.ddh:

=============================
Preventing accidental deletes
=============================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_ddh
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_noi.projects.team.settings.doctests'
    >>> from lino.api.doctest import *


Foreign Keys and their `on_delete` setting
==========================================

Here is the output of :meth:`lino.utils.diag.Analyzer.show_foreign_keys` in
Lino Noi:


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
- clocking.SessionType :
  - PROTECT : clocking.Session.session_type
- contacts.Company :
  - PROTECT : excerpts.Excerpt.company, contacts.Role.company, system.SiteConfig.site_company, tickets.Project.company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Person.partner_ptr, contacts.Company.partner_ptr
  - PROTECT : users.User.partner, lists.Member.partner, outbox.Recipient.partner, tickets.Site.partner
- contacts.Person :
  - PROTECT : excerpts.Excerpt.contact_person, contacts.Role.person, tickets.Project.contact_person
- contacts.RoleType :
  - PROTECT : excerpts.Excerpt.contact_role, contacts.Role.type, tickets.Project.contact_role
- contenttypes.ContentType :
  - PROTECT : excerpts.ExcerptType.content_type, excerpts.Excerpt.owner_type, comments.Comment.owner_type, stars.Star.owner_type, gfks.HelpText.content_type, outbox.Mail.owner_type, outbox.Attachment.owner_type, uploads.Upload.owner_type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, countries.Place.parent
- excerpts.Excerpt :
  - set_on_delete : clocking.ServiceReport.printed_by, tickets.Milestone.printed_by
- excerpts.ExcerptType :
  - PROTECT : excerpts.Excerpt.excerpt_type
- lists.List :
  - PROTECT : lists.Member.list
- lists.ListType :
  - PROTECT : lists.List.list_type
- outbox.Mail :
  - CASCADE : outbox.Recipient.mail, outbox.Attachment.mail
- products.Product :
  - PROTECT : tickets.Ticket.product, tickets.Interest.product
- products.ProductCat :
  - PROTECT : products.Product.cat
- tickets.Milestone :
  - PROTECT : tickets.Ticket.reported_for, tickets.Deployment.milestone
- tickets.Project :
  - PROTECT : excerpts.Excerpt.project, outbox.Mail.project, tickets.Project.parent, tickets.Ticket.project
- tickets.ProjectType :
  - PROTECT : tickets.Project.type
- tickets.Site :
  - PROTECT : clocking.ServiceReport.interesting_for, users.User.user_site, tickets.Milestone.site, tickets.Ticket.site, tickets.Interest.site
- tickets.Ticket :
  - PROTECT : clocking.Session.ticket, tickets.Link.parent, tickets.Ticket.duplicate_of, tickets.Deployment.ticket
- tickets.TicketType :
  - PROTECT : tickets.Ticket.ticket_type
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : excerpts.Excerpt.user, clocking.Session.user, tinymce.TextFieldTemplate.user, comments.Comment.user, stars.Star.user, users.Authority.user, outbox.Mail.user, tickets.Project.assign_to, tickets.Ticket.assigned_to, uploads.Upload.user
<BLANKLINE>
