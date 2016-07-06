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
  - PROTECT : contacts.Role.company, excerpts.Excerpt.company, system.SiteConfig.site_company, tickets.Project.company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Company.partner_ptr, contacts.Person.partner_ptr
  - PROTECT : clocking.ServiceReport.interesting_for, lists.Member.partner, outbox.Recipient.partner, tickets.Site.partner, topics.Interest.partner, users.User.partner
- contacts.Person :
  - PROTECT : contacts.Role.person, excerpts.Excerpt.contact_person, tickets.Project.contact_person
- contacts.RoleType :
  - PROTECT : contacts.Role.type, excerpts.Excerpt.contact_role, tickets.Project.contact_role
- contenttypes.ContentType :
  - PROTECT : changes.Change.object_type, comments.Comment.owner_type, excerpts.Excerpt.owner_type, excerpts.ExcerptType.content_type, gfks.HelpText.content_type, notify.Notification.owner_type, outbox.Attachment.owner_type, outbox.Mail.owner_type, stars.Star.owner_type, uploads.Upload.owner_type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, countries.Place.parent
- excerpts.Excerpt :
  - SET_NULL : clocking.ServiceReport.printed_by, tickets.Milestone.printed_by
- excerpts.ExcerptType :
  - PROTECT : excerpts.Excerpt.excerpt_type
- faculties.Faculty :
  - PROTECT : clocking.Session.faculty, faculties.Competence.faculty, faculties.Faculty.parent, tickets.Ticket.faculty
- lists.List :
  - PROTECT : lists.Member.list
- lists.ListType :
  - PROTECT : lists.List.list_type
- outbox.Mail :
  - CASCADE : outbox.Attachment.mail, outbox.Recipient.mail
- tickets.Milestone :
  - PROTECT : tickets.Deployment.milestone, tickets.Ticket.reported_for
- tickets.Project :
  - PROTECT : excerpts.Excerpt.project, outbox.Mail.project, tickets.Project.parent, tickets.Ticket.project
- tickets.ProjectType :
  - PROTECT : tickets.Project.type
- tickets.Site :
  - PROTECT : tickets.Milestone.site, tickets.Ticket.site, users.User.user_site
- tickets.Ticket :
  - PROTECT : clocking.Session.ticket, tickets.Deployment.ticket, tickets.Link.parent, tickets.Ticket.duplicate_of
- tickets.TicketType :
  - PROTECT : tickets.Ticket.ticket_type
- topics.Topic :
  - PROTECT : faculties.Competence.topic, tickets.Ticket.topic, topics.Interest.topic
- topics.TopicGroup :
  - PROTECT : faculties.Faculty.topic_group, topics.Topic.topic_group
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : changes.Change.user, clocking.ServiceReport.user, clocking.Session.user, comments.Comment.user, excerpts.Excerpt.user, faculties.Competence.user, notify.Notification.user, outbox.Mail.user, stars.Star.user, tickets.Project.assign_to, tickets.Ticket.assigned_to, tinymce.TextFieldTemplate.user, uploads.Upload.user, users.Authority.user
<BLANKLINE>
