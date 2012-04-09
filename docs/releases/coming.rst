Coming
======

Sichtbare Änderungen
--------------------

- Neue Tabelle :class:`Offene Kursanfragen 
  <lino.apps.pcsw.courses.models.PendingCourseRequests>`.
  
- Änderungen in :class:`Übersicht Art-60-7-Konventionen <jobs.JobsOverview>`:

  - die aktiven Stellenbesetzer sind jetzt nach `Contract.applies_from` 
    (Beginndatum des Vertrags) sortiert. 
    Bisher war die Reihenfolge zufällig.
    
  - die Kandidaten sind jetzt nach `Candidature.date_submitted` 
    (Datum der Anfrage) sortiert. Bisher war die Reihenfolge zufällig.
    
  - In "Kandidaten" wurden fälschlicherweise auch Personen angezeigt, 
    die nicht mehr begleitet sind (aber für die eine Stellenanfrage gemacht 
    worden war).
  
- Art 60/7 Konvention Enddatum: soll immer 1 Tag früher sein als jetzt.
  zB: 01/01/2012 bis 31/12/2013 und nicht bis 01/01/2013
  
- Datenkontrollliste für *alle* Klienten (wenn "nur aktive am" leer ist) 
  schien bisher durch einen Timeout von 30 Sekunden leer. Behoben.


Bugfixes
--------

- :class:`Übersicht Art-60-7-Konventionen <jobs.JobsOverview>`: 
  das Datum der Liste stand fälschlicherweise par défaut immer 
  auf dem Tag, an dem die lino.js zuletzt generiert worden war 
  (d.h. praktisch das Datum des letzten Releases). 
  Jetzt ist das Feld par défaut leer (was dann "heute" bedeutet).

- Beim Speichern einer Notiz, für die ein Drittparter existierte, kam eine Fehlermeldung “Ajax communication failed”.

- Felder eID-Karte gültig von und gültig bis waren zu klein.

- Wenn man z.B. in der Liste der Stellen 
  auf einen Stellenanbieter klickte um dessen Detail zu sehen, 
  kam stattdessen ein Traceback auf dem Server.
  (:doc:`/blog/2012/0305`)
  
- Die "(zeigen)"-Links im Detail Organisation und Person 
  funktionierten nicht. 
  (:doc:`/blog/2012/0305`)
  
- "Remote fields" funktionierte noch nicht. 
  Kamen allerdings bisher nur in 
  :menuselection:`Stellen --> Suche Art-60-7-Konventionen` vor (Kolonnen Stadt, NR-Nummer und Geschlecht)
  Auch der :guilabel:`[html]`-Button in diesen Tabellen funktionierte nicht.

- Wenn man z.B. in der Liste der Stellen auf einen Stellenanbieter klickte 
  um dessen Detail zu sehen, kam stattdessen eine Fehlermeldung 
  "TypeError at /api/jobs/JobProviderTable/3999 / 
  unsupported operand type(s) for +: 'NoneType' and 'unicode'"
  
- die “(zeigen)”-Links im Detail Organisation und Person funktionierten nicht. 
  

Internal changes
----------------

Administrators need to ``aptitude install python-lxml`` before upgrading.
:mod:`lino.utils.xmlgen` turned out to be a reinvention of the wheel 
and has been replaced by `lxml <http://www.lxml.de>`_.

