.. _noi.specs.care:

==============================
The "Care" variant of Lino Noi
==============================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_care
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.care.settings.doctests')
    >>> from lino.api.doctest import *



Overview
========

Lino Care is a variant of Lino Noi specialized for organizations which
help people to care for each other.  These people might be old people,
orphans, immigrants, disabled, addicts, or just "normal" people
without any "handicap".

- There is no difference between **care recipients** and **care
  providers**.  Both are stored as *system users*.  Any user can "call
  for help" by "opening a ticket". This is similar to the known
  ticketing systems of a softare project. A different context, but a
  similar database structure.

  Users can also enter information about their **competences** and
  their **availability**.

  This does not mean that these people actually have access to
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


Users
=====

These user roles are defined in :mod:`lino_noi.projects.care.roles`

>>> rt.show('users.UserProfiles')
====== =========== ===========
 Wert   name        Text
------ ----------- -----------
 000    anonymous   Anonym
 100    user        Benutzer
 500    manager     Manager
 900    admin       Verwalter
====== =========== ===========
<BLANKLINE>

>>> rt.show('users.Users')
============== ================ ========= ==============
 Benutzername   Benutzerprofil   Vorname   Familienname
-------------- ---------------- --------- --------------
 anna           Benutzer
 berta          Benutzer
 christina      Benutzer
 dora           Benutzer
 robin          Verwalter        Robin     Rood
 rolf           Verwalter        Rolf      Rompen
 romain         Verwalter        Romain    Raffault
============== ================ ========= ==============
<BLANKLINE>



Faculties
=========

She site has a list of **faculties** (or however one might call
the "needed services or things" which will make the connection
recipient and provider of help.

Their actual name can be locally configured by setting the
verbose_name and verbose_name_plural options of `faculties.Faculty`.

>>> rt.show('faculties.Faculties')
==== ========== ========= ========================= ============================= ================== ============================ ========== ====================
 ID   Referenz   Nr.       Übergeordnete Fähigkeit   Bezeichnung                   Bezeichnung (en)   Bezeichnung (fr)             Affinity   Optionen-Kategorie
---- ---------- --------- ------------------------- ----------------------------- ------------------ ---------------------------- ---------- --------------------
 1               1                                   Analysis                                                                      100
 2               2                                   Code changes                                                                  100
 3               3                                   Documentation                                                                 100
 4               4                                   Testing                                                                       100
 5               5                                   Configuration                                                                 100
 6               6                                   Enhancement                                                                   100
 7               7                                   Optimization                                                                  100
 8               8                                   Offer                                                                         100
 9               9                                   Unterricht                                       Cours                        100
 10              1         Unterricht                Französischunterricht                            Cours de francais            100
 11              2         Unterricht                Deutschunterricht                                Cours d'allemand             100
 12              3         Unterricht                Matheunterricht                                  Cours de maths               100
 13              4         Unterricht                Gitarrenunterricht                               Cours de guitare             100
 14              10                                  Nähen                                            Couture                      100
 15              11                                  Friseur                                          Coiffure                     100
 16              12                                  Gartenarbeiten                                   Travaux de jardin            100
 17              13                                  Fahrdienst                                       Voiture                      100
 18              14                                  Botengänge                                       Commissions                  100
 19              15                                  Babysitting                                      Garde enfant                 100
 20              16                                  Gesellschafter für Senioren                      Rencontres personnes agées   100
 21              17                                  Hunde spazierenführen                            Chiens                       100
 22              18                                  Übersetzungsarbeiten                             Traductions                  100        Sprachen
 23              19                                  Briefe beantworten                               Répondre au courrier         100
                 **200**                                                                                                           **2300**
==== ========== ========= ========================= ============================= ================== ============================ ========== ====================
<BLANKLINE>

>>> rt.show('faculties.Competences')
==== ========== ====================== ========== =============
 ID   Benutzer   Fähigkeit              Affinity   Option
---- ---------- ---------------------- ---------- -------------
 1    anna       Übersetzungsarbeiten   100        Französisch
 2    berta      Übersetzungsarbeiten   100        Französisch
 3    berta      Übersetzungsarbeiten   100        Deutsch
                                        **300**
==== ========== ====================== ========== =============
<BLANKLINE>

>>> rt.show('topics.Topics')
========== ============= ================== ================== ==============
 Referenz   Bezeichnung   Bezeichnung (en)   Bezeichnung (fr)   Themengruppe
---------- ------------- ------------------ ------------------ --------------
            Französisch   French             Français           Sprachen
            Deutsch       German             Allemand           Sprachen
            Englisch      English            Anglais            Sprachen
========== ============= ================== ================== ==============
<BLANKLINE>


>>> rt.show('tickets.Tickets')
==== =========================================================================================== ======= =============== =========== =========
 ID   Summary                                                                                     Thema   Arbeitsablauf   Anfrager    Projekt
---- ------------------------------------------------------------------------------------------- ------- --------------- ----------- ---------
 6    Wer fährt für mich nach Aachen Pampers kaufen?                                                      **Erledigt**    anna
 5    Wer kann meine Abschlussarbeit korrekturlesen?                                                      **Sleeping**    dora
 4    Wer hilft meinem Sohn sich auf die Mathearbeit am 21.05. vorzubereiten? 5. Schuljahr PDS.           **Sticky**      berta
 3    Wer kommt meinem Sohn Klavierunterricht geben?                                                      **ToDo**        dora
 2    Mein Rasen muss gemäht werden. Donnerstags oder Samstags                                            **Talk**        christina
 1    Mein Wasserhahn tropft, wer kann mir helfen?                                                        **Neu**         berta
==== =========================================================================================== ======= =============== =========== =========
<BLANKLINE>
