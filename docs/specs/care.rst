.. _noi.specs.care:

==============================
The "Care" variant of Lino Noi
==============================

Implementation notes
====================

The "Care" project is currently in a very early stage. We are still
thinking about whether at all to implement it (1) as a variant of Lino
Noi or (b) by writing a new application from scratch. Hamza and Luc
are keeping an eye but not actively working on approach (1) while
Sandeep (with Luc's help) is working on approach (2).

Overview
========

The site owner is an organization which cares for people and helps
people to care for each other.  These people might be old people,
orphans, immigrants, disabled, addicts, or just "normal" people
(i.e. without any "handicap") because also normal people might want to
help each other.

- The site has a list of **care recipients**. A care recipient can
   "call for help" by "opening a ticket". This is similar to the known
   ticketing systems of a softare project. A different context, but a
   similar database structure.

- The site also has a list of **care providers**. Care providers enter
  information about their **competences** and their **availability**.

  Both care recipients and providers are stored as *system
  users*. This does not mean that these people actually have access to
  the Lino site. It is possible that some "**manager**" does the job of
  entering the information into Lino.

- And then the site maintains a "catalogue" of "needed services or
  things" which will make the connection recipient and provider. For
  example things like "table" or "a pair of shoes", or services like
  "Baby sitting", "English teaching" or "Pedicure".

- The application protects privacy of all users as much as
  possible. Neither providers nor recipients are listed publicly. All
  users must be confirmed after registration. There is a manager (one
  person or a team of several users) who does this job. The manager
  can see all users and their data.

- The care recipients can create new tickets and enter information
  about what kind of care they need. They cannot see who is going to
  help them. They cannot even see whether somebody is available at all
  for a given type of care.

- The care providers can see the incoming help requests for the kind
  of thing or service they provide. They can see the contact data of
  the user who asks for help.

  When they receive a notification about a help request, they must
  give feedback, e.g. they can *refuse* it (possibly specifying a
  reason like "I am not available" or "Request does not fit to what I
  can give").  If they decide to contact that person, then they should
  register this to the database: date and time of contact, a field for
  remarks, and (important) whether they decided to "take the ticket"
  or not after speaking with the recipient.

- Depending on the nature of the "service or thing", there must
  probably be additional information.


Using a variant of Lino Noi
===========================

While Lino Noi was originally planned as a ticketing system for the
Lino team (and other teams who work similarily), the
:mod:`lino_noi.projects.care` project might be a cool application for
the Care project.  

- And the site has a list of **faculties** (or however one might call
  the "needed services or things" which will make the connection
  recipient and provider. 

  Their actual name can be locally configured
  by setting the verbose_name and verbose_name_plural options of
  `faculties.Faculty`.



  These user roles are defined in :mod:`lino_noi.projects.care.roles`

