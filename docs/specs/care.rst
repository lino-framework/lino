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
====== =========== ============
 Wert   name        Text
------ ----------- ------------
 000    anonymous   Anonym
 100    user        Benutzer
 500    connector   Vermittler
 900    admin       Verwalter
====== =========== ============
<BLANKLINE>


>>> rt.show('users.Users')
============== ================ ========= ==============
 Benutzername   Benutzerprofil   Vorname   Familienname
-------------- ---------------- --------- --------------
 axel           Benutzer
 berta          Benutzer
 christa        Benutzer
 dora           Benutzer
 eric           Benutzer
 robin          Verwalter        Robin     Rood
 rolf           Verwalter        Rolf      Rompen
 romain         Verwalter        Romain    Raffault
============== ================ ========= ==============
<BLANKLINE>



Faculties
=========

She site has a list of **faculties**, i.e. the "needed services or
things" which will make the connection between recipient and provider
of help.

Every ticket can require a given faculty.  When assigning a worker to
such a ticket, Lino will suggest only users having a competence for
this faculty.

A faculty is something a user must be able to do in order to work on
this ticket.


Their actual name can be locally configured by setting the
verbose_name and verbose_name_plural options of `faculties.Faculty`.

>>> rt.show(faculties.AllFaculties)
... #doctest: +REPORT_UDIFF
============================= ================== ============================ =========== ==================== =========================
 Bezeichnung                   Bezeichnung (en)   Bezeichnung (fr)             Affinität   Optionen-Kategorie   Übergeordnete Fähigkeit
----------------------------- ------------------ ---------------------------- ----------- -------------------- -------------------------
 Babysitting                                      Garde enfant                 100
 Botengänge                                       Commissions                  100
 Briefe beantworten                               Répondre au courrier         100
 Deutschunterricht                                Cours d'allemand             100                              Unterricht
 Fahrdienst                                       Voiture                      100
 Französischunterricht                            Cours de francais            100                              Unterricht
 Friseur                                          Coiffure                     100
 Gartenarbeiten                                   Travaux de jardin            100                              Haus und Garten
 Gesellschafter für Senioren                      Rencontres personnes agées   100
 Gitarrenunterricht                               Cours de guitare             100                              Musik
 Handwerksarbeiten                                Travaux de réparation        100                              Haus und Garten
 Haus und Garten                                  Maison et jardin             100
 Hunde spazierenführen                            Chiens                       100
 Klavierunterricht                                Cours de piano               100                              Musik
 Matheunterricht                                  Cours de maths               100                              Unterricht
 Musik                                            Musique                      100
 Nähen                                            Couture                      100                              Haus und Garten
 Unterricht                                       Cours                        100
 Übersetzungsarbeiten                             Traductions                  100         Sprachen
 **Total (19 Zeilen)**                                                         **1900**
============================= ================== ============================ =========== ==================== =========================
<BLANKLINE>


>>> rt.show(faculties.TopLevelFaculties)
... #doctest: +REPORT_UDIFF
======== ============================= ================== ============================ ================================================================= =========================
 Nr.      Bezeichnung                   Bezeichnung (en)   Bezeichnung (fr)             Kinder                                                            Übergeordnete Fähigkeit
-------- ----------------------------- ------------------ ---------------------------- ----------------------------------------------------------------- -------------------------
 1        Unterricht                                       Cours                        *Französischunterricht*, *Deutschunterricht*, *Matheunterricht*
 2        Musik                                            Musique                      *Gitarrenunterricht*, *Klavierunterricht*
 3        Haus und Garten                                  Maison et jardin             *Nähen*, *Gartenarbeiten*, *Handwerksarbeiten*
 4        Fahrdienst                                       Voiture
 5        Botengänge                                       Commissions
 6        Friseur                                          Coiffure
 7        Babysitting                                      Garde enfant
 8        Gesellschafter für Senioren                      Rencontres personnes agées
 9        Hunde spazierenführen                            Chiens
 10       Übersetzungsarbeiten                             Traductions
 11       Briefe beantworten                               Répondre au courrier
 **66**
======== ============================= ================== ============================ ================================================================= =========================
<BLANKLINE>


>>> rt.show('faculties.Competences')
==== ========== ====================== =========== =============
 ID   Benutzer   Fähigkeit              Affinität   Option
---- ---------- ---------------------- ----------- -------------
 1    axel       Übersetzungsarbeiten   100         Französisch
 2    berta      Übersetzungsarbeiten   100         Französisch
 3    berta      Übersetzungsarbeiten   100         Deutsch
 4    axel       Botengänge             100
 5    axel       Handwerksarbeiten      100
 6    christa    Klavierunterricht      100
 7    eric       Gitarrenunterricht     100
                                        **700**
==== ========== ====================== =========== =============
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
==== =========================================================================================== ========== ======= ==================== ================ =========
 ID   Zusammenfassung                                                                             Anfrager   Thema   Fähigkeit            Arbeitsablauf    Projekt
---- ------------------------------------------------------------------------------------------- ---------- ------- -------------------- ---------------- ---------
 8    Wer fährt für mich nach Aachen Pampers kaufen?                                              axel               Botengänge           **Storniert**
 7    Wer kann meine Abschlussarbeit korrekturlesen?                                              dora                                    **Erledigt**
 6    Wer hilft meinem Sohn sich auf die Mathearbeit am 21.05. vorzubereiten? 5. Schuljahr PDS.   berta              Matheunterricht      **Bereit**
 5    Wer macht Musik auf meinem Geburtstag am 12.12.2012 ?                                       axel               Musik                **Schläft**
 4    Wer kann meiner Tochter Gitarreunterricht geben?                                            axel               Gitarrenunterricht   **Sticky**
 3    Wer kann meinem Sohn Klavierunterricht geben?                                               dora               Klavierunterricht    **ZuTun**
 2    Mein Rasen muss gemäht werden. Donnerstags oder Samstags                                    christa                                 **Besprechen**
 1    Mein Wasserhahn tropft, wer kann mir helfen?                                                berta              Handwerksarbeiten    **Neu**
==== =========================================================================================== ========== ======= ==================== ================ =========
<BLANKLINE>


TODO: show how the choices for Ticket.assigned_to depend on faculty
and topic.

The main menu
=============


In :ref:`care` we don't call them "tickets" but "pleas" (German
"Bitten").

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Büro : Meine Benachrichtigungen, Meine Favoriten, Meine Auszüge, Meine Kommentare
- Bitten : Meine Bitten, Wo ich helfen kann, Zu tun, Aktive Bitten, Bitten, Nicht zugewiesene Bitten, Aktive Projekte
- Arbeitszeit : Sitzungen
- Berichte :
  - System : Broken GFKs
  - Arbeitszeit : Dienstleistungsberichte
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Benutzer : Themen, Themengruppen
  - Büro : Auszugsarten, Meine Einfügetexte
  - Bitten : Projekte, Projekte (Hierarchie), Project Types, Ticket types, Umfelder
  - Fähigkeiten : Fähigkeiten (Hierarchie), Fähigkeiten (alle)
  - Arbeitszeit : Session Types
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerprofile, Benachrichtigungen, Änderungen
  - Benutzer : Interessen
  - Büro : Favoriten, Auszüge, Kommentare, Einfügetexte
  - Bitten : Verknüpfungen, Zustände
  - Fähigkeiten : Kompetenzen
  - Arbeitszeit : Sitzungen
- Site : Info


**Simple** users have a very limited menu:

>>> rt.login('berta').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Büro : Meine Benachrichtigungen, Meine Favoriten, Meine Auszüge, Meine Kommentare
- Bitten : Meine Bitten, Wo ich helfen kann, Zu tun
- Konfigurierung :
 - Orte : Länder
 - Büro : Meine Einfügetexte
- Site : Info


Pleas (Tickets)
===============

  
>>> rt.login('christa').show(tickets.MyTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================================================================ =========== ======= ==============================================
 Overview                                                                     Fähigkeit   Thema   Arbeitsablauf
---------------------------------------------------------------------------- ----------- ------- ----------------------------------------------
 `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__                       **Besprechen** → [🐜] [🕸] [☐] [☑] [🗑] [✋] [☆]
============================================================================ =========== ======= ==============================================
<BLANKLINE>


>>> rt.login('christa').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
========================================================================= ========== ======= =================== =======================
 Overview                                                                  Anfrager   Thema   Fähigkeit           Arbeitsablauf
------------------------------------------------------------------------- ---------- ------- ------------------- -----------------------
 `#5 (Wer macht Musik auf meinem Geburtstag am 12.12.2012 ?) <Detail>`__   axel               Musik               **Schläft** → [✋] [☆]
 `#3 (Wer kann meinem Sohn Klavierunterricht geben?) <Detail>`__           dora               Klavierunterricht   **ZuTun** → [✋] [☆]
========================================================================= ========== ======= =================== =======================
<BLANKLINE>


>>> rt.login('christa').show(tickets.TicketsToDo)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Keine Daten anzuzeigen


Rating a ticket
===============

>>> base = '/choices/tickets/Tickets/rating'
>>> show_choices("robin", base + '?query=')
<br/>
Very good
Good
Satisfying
Deficient
Insufficient
Unratable

>>> show_choices("rolf", base + '?query=')
<br/>
Sehr gut
Gut
Ausreichend
Mangelhaft
Ungenügend
Nicht bewertbar

>>> show_choices("romain", base + '?query=')
<br/>
Très bien
Bien
Satisfaisant
Médiocre
Insuffisant
Nicht bewertbar
