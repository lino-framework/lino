Coming
======

New features
------------

- Neues Modul "Kalender".
  Sh. :doc:`/blog/2011/0625` und :doc:`/blog/2011/0627`.
  Wichtigste Änderungen, die die Bentzer betreffen:
  
  - In Notizen und Verträgen gibt es die Felder "Fällig am" 
    bis "erledigt" jetzt nicht mehr, sondern stattdessen eine Tabelle 
    von "Aufgaben", die dieser Notiz bzw. diesem Vertrag zugeordnet sind.
  - Im Detail einer Person gibt es jetzt einen neuen Reiter "Kalender", 
    in dem zwei Tabellen sind: Aufgaben und Termine dieser Person. 
    Die Termine werden wir bis auf weiteres noch nicht benutzen (sind noch 
    nicht synchronisiert mit GroupWise).
    
  - Im Hauptmenü gibt es einen neuen Befehl "Meine Aufgaben", der alle 
    Aufgaben des Benutzers anzeigt.
  - Die unerledigten Aufgaben sind es auch, die auf der Startseite angezeigt 
    werden.

- Kleine Änderungen in der Übersichtstabelle auf der Startseite 
  (`persons_by_user`)
  
- Ein erstes Listing "Situation Verträge"

- Standardfilter : Inaktive Personen nicht anzeigen in 
  :menuselection:`Kontakte --> Personen` und Auswahllisten.
  Um eine inaktive Person aktiv zu machen: entweder einen 
  bestehenden Record finden, der auf die Person verweist und dort 
  deren Detail aufrufen, oder :menuselection:`Konfigurierung --> 
  Explorer --> Personen (alle)`.
  Sh. :doc:`/blog/2011/0701`.

- Kontrollliste. 
  Wenn Person.national_id nicht leer ist, muss es jetzt eine gültige 
  belgische Nationalregisternummer (NISS) sein. Das ist allerdings 
  keine "harte" Bedingung (führt nicht zu einem database integrity error), 
  sondern lediglich zu einer Warnung in der neuen "Kontrollliste".
  Auslöser war watch_tim, der eine Firma zur Person machte, 
  weil sie in PAR->NB2 versehentlich einen Wert drinstehen hatte 
  (der aber keine NISS war). 
  Solchen Fälle ersehen wir also zukünftig wenigstens aus der 
  Kontrollliste. 
  Sh. :doc:`/blog/2011/0712`.


Internal optimizations
----------------------

- :term:`watch_tim` now logs changes of `lino.utils.DiffingMixin` 
  instances (e.g. :class:`lino.apps.dsbe.models.Person`, :class:`lino.apps.dsbe.models.Contract`)
  
- Some API refinements to be used in AppyPrintMethod document templates
  (e.g. `iif`, `Person.get_skills`, ...)
  

Bugs fixed
----------

- :term:`watch_tim` ignorierte das Leeren eines Feldes (:doc:`/blog/2011/0711`)

Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.


- Database migration: 

