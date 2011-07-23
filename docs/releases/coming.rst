Lino 1.2.0 (Coming)
===================

New features
------------

- **Listing "Situation Verträge"**. 
  Für dieses Listing waren einige Erweiterungen der Datenbankstruktur nötig.

  Es gibt jetzt eine konfigurierbare Liste von **Stellen**. 
  Eine "Stelle" ist ein Arbeitsplatz bei einem bestimmten Stellenanbieter, 
  für den das ÖSHZ Kandidaten sucht und Verträge erstellt. 
  Stellen sind nicht nur die 
  Art.60-7-Stellen, sondern auch VSE und interne Stellen.
  Beim Erstellen eines Vertrags muss man nun vor allem diese Stelle angeben. 
  In den meisten Fällen braucht man dann die Organisation 
  und die Vertragsart nicht mehr einzugeben, weil die pro Stelle 
  konfiguriert sind.
  
  Die bestehenden Verträge haben bei der Datenmigration eine Serie 
  von ca. 30 Stellen erzeugt, die nach dem Release manuell überprüft 
  werden müssen.
  
  Man kann von einer Person aus "Vertragsanfragen" erstellen. 
  Eine Vertragsanfrage ist, wenn eine bestimmte Person als Kandidat 
  für eine bestimmte Stelle in Frage kommt.
  
  Details siehe :doc:`/blog/2011/0716`
    
- Neues Modul **Kalender**.
  Auch hier einige Änderungen, die die Benutzer betreffen:
  
  In Notizen, Verträgen, Uploads und Links gibt es jetzt nicht mehr 
  die 5 Felder "Fällig am", "Erinnerungstext", ... "erledigt", 
  sondern stattdessen eine Tabelle von "Aufgaben", die diesem 
  Objekt zugeordnet sind.
  **Eine Notiz kann also jetzt mehr als eine Erinnerung hervorrufen.**
  Im Hauptmenü gibt es einen neuen Befehl "Meine Aufgaben", der alle 
  Aufgaben des Benutzers anzeigt.
  Die unerledigten Aufgaben sind es auch, die auf der Startseite angezeigt 
  werden.
  
  Es gibt auch eine Tabelle von Aufgaben *pro Person*. 
  Dort stehen auch alle Aufgaben, die der Person indirekt durch 
  eine Notiz oder einen Vertrag zugewiesen wurden.
    
  Die Termine werden wir bis auf weiteres noch nicht benutzen (sind noch 
  nicht synchronisiert mit GroupWise).

  Details siehe :doc:`/blog/2011/0625` und :doc:`/blog/2011/0627`.
  
- **Standardfilter** : Inaktive Personen nicht anzeigen in 
  :menuselection:`Kontakte --> Personen` und Auswahllisten.
  Um eine inaktive Person aktiv zu machen: entweder einen 
  bestehenden Record finden, der auf die Person verweist und dort 
  deren Detail aufrufen, oder :menuselection:`Konfigurierung --> 
  Explorer --> Personen (alle)`.
  Sh. :doc:`/blog/2011/0701`.

- **Kontrollliste**. 
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
  
- **Einfügetexte** :
  im Text-Editor gibt es jetzt einen neuen Button "Inhalt aus Vorlage einfügen".
  Jeder Benutzer kann über
  :menuselection:`Mein Menu --> Meine Einfügetexte`
  seine eigene Sammlung von Einfügetexten pflegen.
  *Öffentliche* Einfügetexte (d.h. mit leerem Feld "Benutzer")
  können von jedem eingefügt, aber nur vom Systemverwalter bearbeitet 
  werden (über :menuselection:`Konfigurierung --> System --> Einfügetexte`).
  
  Ich warte auf erste Erfahrungsberichte, bevor ich kontextabhängige 
  Auswahl einbaue.
  
  Details siehe :doc:`/blog/2011/0722`

- Kleine Änderungen in der Übersichtstabelle auf der Startseite 
  (`persons_by_user`)
  
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

- Database migration

- Install TinyMCE language packs if necessary

